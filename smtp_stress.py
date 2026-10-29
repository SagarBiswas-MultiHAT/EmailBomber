#!/usr/bin/env python3
"""
SMTP Stress Bench - High-Performance Mail Server Load & Resilience Testing Suite
Copyright (C) 2026 Sagar Biswas. All rights reserved.
SPDX-License-Identifier: GPL-3.0-or-later

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import argparse
import concurrent.futures
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
import os
import re
import smtplib
import ssl
import sys
import threading
import time

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
PRINT_LOCK = threading.Lock()


def load_dotenv_fallback(dotenv_path: str = ".env"):
    """Load configuration from .env into os.environ if not already defined."""
    if not os.path.isfile(dotenv_path):
        return
    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                if key and key not in os.environ:
                    os.environ[key] = val
    except Exception:
        pass


def validate_email(email: str) -> bool:
    """Validate email address format."""
    return bool(EMAIL_REGEX.match(email.strip()))


class BenchmarkMetrics:
    """Thread-safe metrics accumulator for SMTP benchmarking."""

    def __init__(self, total_expected: int):
        self.total_expected = total_expected
        self.successful = 0
        self.failed = 0
        self.latencies = []
        self.errors = {}
        self.start_time = 0.0
        self.end_time = 0.0
        self._lock = threading.Lock()

    def start(self):
        self.start_time = time.perf_counter()

    def record_success(self, latency_ms: float):
        with self._lock:
            self.successful += 1
            self.latencies.append(latency_ms)

    def record_failure(self, error_message: str):
        with self._lock:
            self.failed += 1
            clean_error = error_message.split("\n")[0][:60]
            self.errors[clean_error] = self.errors.get(clean_error, 0) + 1

    def stop(self):
        self.end_time = time.perf_counter()

    def get_progress_counts(self):
        with self._lock:
            return self.successful + self.failed

    def print_summary(self):
        elapsed = self.end_time - self.start_time if self.end_time > 0 else 0.001
        with self._lock:
            avg_latency = (sum(self.latencies) / len(self.latencies)) if self.latencies else 0.0
            min_latency = min(self.latencies) if self.latencies else 0.0
            max_latency = max(self.latencies) if self.latencies else 0.0
            throughput = self.successful / elapsed if elapsed > 0 else 0.0
            completion_rate = (self.successful / self.total_expected * 100) if self.total_expected else 0.0

            print("\n" + "=" * 65)
            print("                 SMTP BENCHMARK SUMMARY REPORT")
            print("=" * 65)
            print(f" Total Requests Scheduled : {self.total_expected}")
            print(f" Successful Deliveries    : {self.successful} ({completion_rate:.1f}%)")
            print(f" Failed Deliveries        : {self.failed}")
            print(f" Total Elapsed Time       : {elapsed:.2f} seconds")
            print(f" Effective Throughput     : {throughput:.2f} emails/sec")
            print("-" * 65)
            print(f" Min Latency              : {min_latency:.2f} ms")
            print(f" Avg Latency              : {avg_latency:.2f} ms")
            print(f" Max Latency              : {max_latency:.2f} ms")
            print("-" * 65)

            if self.errors:
                print(" Failure Breakdown:")
                for err, count in self.errors.items():
                    print(f"   * [{count}x] {err}")
                print("-" * 65)

            print(" Benchmark test finished.\n")


def build_message(sender: str, recipient: str, subject: str, body_text: str, is_html: bool = False) -> str:
    """Construct a MIME multipart email string."""
    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg["X-Mailer"] = "SMTP-Stress-Bench/1.0.0"

    content_type = "html" if is_html else "plain"
    msg.attach(MIMEText(body_text, content_type, "utf-8"))
    return msg.as_string()


def create_smtp_connection(host: str, port: int, use_tls: bool, use_ssl: bool, timeout: int = 15):
    """Establish and return an active SMTP connection."""
    if use_ssl:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(host, port, timeout=timeout, context=context)
    else:
        server = smtplib.SMTP(host, port, timeout=timeout)
        if use_tls:
            server.ehlo()
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.ehlo()
    return server


def worker_send_task(worker_id: int, iterations: int, delay: float, config: dict, metrics: BenchmarkMetrics):
    """Worker function to dispatch batch emails with latency tracking."""
    host = config["host"]
    port = config["port"]
    sender = config["sender"]
    recipient = config["recipient"]
    password = config.get("password")
    use_tls = config["use_tls"]
    use_ssl = config["use_ssl"]
    subject = config["subject"]
    body = config["body"]
    is_html = config["is_html"]

    server = None
    try:
        server = create_smtp_connection(host, port, use_tls, use_ssl)
        if password:
            server.login(sender, password)

        for i in range(iterations):
            try:
                iter_subject = f"{subject} [Iter #{worker_id}-{i + 1}]"
                raw_msg = build_message(sender, recipient, iter_subject, body, is_html)

                t_start = time.perf_counter()
                server.sendmail(sender, [recipient], raw_msg)
                t_end = time.perf_counter()

                latency_ms = (t_end - t_start) * 1000.0
                metrics.record_success(latency_ms)

                total_done = metrics.get_progress_counts()
                with PRINT_LOCK:
                    print(f" [{total_done:>4}/{metrics.total_expected}] Worker {worker_id:<2} sent email {i + 1:<4} in {latency_ms:>7.2f} ms")

            except Exception as send_err:
                metrics.record_failure(str(send_err))
                with PRINT_LOCK:
                    print(f" [FAIL] Worker {worker_id:<2} iteration {i + 1} failed: {send_err}")

            if delay > 0 and i < iterations - 1:
                time.sleep(delay)

    except Exception as conn_err:
        for _ in range(iterations):
            metrics.record_failure(f"Connection/Auth error: {conn_err}")
        with PRINT_LOCK:
            print(f" [CRITICAL] Worker {worker_id} connection failed: {conn_err}")

    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass


def interactive_wizard() -> dict:
    """Prompt user interactively for benchmark configuration."""
    print("\n" + "=" * 65)
    print("       SMTP Stress Bench - Interactive Setup Wizard")
    print("=" * 65)

    host = input(" SMTP Server Host [smtp.gmail.com]: ").strip() or "smtp.gmail.com"
    default_port = 587
    port_in = input(f" SMTP Server Port [{default_port}]: ").strip()
    port = int(port_in) if port_in else default_port

    use_ssl = port == 465
    use_tls = not use_ssl

    while True:
        sender = input(" Sender Email Address: ").strip()
        if validate_email(sender):
            break
        print(" [!] Invalid email address. Please try again.")

    password = getpass(" Sender Password / App Password (leave blank if unauthenticated): ")

    while True:
        recipient = input(" Recipient / Test Inbox Address: ").strip()
        if validate_email(recipient):
            break
        print(" [!] Invalid email address. Please try again.")

    count_in = input(" Total Number of Emails to Send [10]: ").strip()
    count = int(count_in) if count_in else 10

    delay_in = input(" Delay Between Sends (seconds) [0.5]: ").strip()
    delay = float(delay_in) if delay_in else 0.5

    concurrency_in = input(" Concurrency (worker threads) [1]: ").strip()
    concurrency = int(concurrency_in) if concurrency_in else 1

    subject = input(" Email Subject [SMTP Benchmark Test]: ").strip() or "SMTP Benchmark Test"

    format_choice = input(" Content Format - 1 for Text, 2 for HTML [1]: ").strip()
    is_html = format_choice == "2"

    if is_html:
        body = """<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #0066cc;">SMTP Load Benchmark Test</h2>
    <p>This automated test message was generated by <strong>SMTP Stress Bench</strong>.</p>
    <div style="background: #f4f4f4; padding: 12px; border-left: 4px solid #0066cc;">
        <p><strong>Status:</strong> Active Test Transmission</p>
        <p><strong>Timestamp:</strong> Generated during server resilience verification.</p>
    </div>
    <p style="font-size: 12px; color: #888;">Authorized benchmarking transmission.</p>
</body>
</html>"""
    else:
        body = "This is an automated performance benchmark message generated by SMTP Stress Bench."

    return {
        "host": host,
        "port": port,
        "sender": sender,
        "recipient": recipient,
        "password": password,
        "count": count,
        "delay": delay,
        "concurrency": concurrency,
        "use_tls": use_tls,
        "use_ssl": use_ssl,
        "subject": subject,
        "body": body,
        "is_html": is_html,
    }


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    load_dotenv_fallback()

    parser = argparse.ArgumentParser(
        description="SMTP Stress Bench: Mail Server Load Testing & Resilience Benchmarking Tool",
        epilog="Licensed under GNU General Public License v3.0 (GPL-3.0). Copyright (C) 2026 Sagar Biswas."
    )

    parser.add_argument("-H", "--host", default=os.getenv("SMTP_HOST", ""), help="SMTP server hostname (default: smtp.gmail.com or env SMTP_HOST)")
    parser.add_argument("-P", "--port", type=int, default=int(os.getenv("SMTP_PORT", "0")), help="SMTP server port (e.g. 587, 465, 25, 1025)")
    parser.add_argument("-s", "--sender", default=os.getenv("SMTP_USER", ""), help="Sender email address")
    parser.add_argument("-r", "--recipient", default="", help="Target recipient or test inbox address")
    parser.add_argument("-p", "--password", default=os.getenv("SMTP_PASSWORD", ""), help="SMTP password or app password")
    parser.add_argument("-n", "--count", type=int, default=10, help="Total number of emails to dispatch (default: 10)")
    parser.add_argument("-c", "--concurrency", type=int, default=1, help="Concurrent worker threads (default: 1)")
    parser.add_argument("-d", "--delay", type=float, default=0.5, help="Delay between emails per worker in seconds (default: 0.5)")
    parser.add_argument("--ssl", action="store_true", help="Connect using direct SSL/TLS (port 465)")
    parser.add_argument("--no-tls", action="store_true", help="Disable STARTTLS (for plain local testing on port 25/1025)")
    parser.add_argument("--subject", default="SMTP Benchmark Test Message", help="Custom email subject line")
    parser.add_argument("--html", action="store_true", help="Send formatted HTML payload instead of plaintext")
    parser.add_argument("-i", "--interactive", action="store_true", help="Launch interactive step-by-step wizard")

    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.interactive or (not args.sender and not args.recipient):
        config = interactive_wizard()
    else:
        host = args.host or "smtp.gmail.com"
        port = args.port if args.port > 0 else (465 if args.ssl else 587)
        use_ssl = args.ssl or port == 465
        use_tls = not use_ssl and not args.no_tls

        sender = args.sender
        if not sender:
            sender = input("Sender Email Address: ").strip()

        recipient = args.recipient
        if not recipient:
            recipient = input("Recipient Address: ").strip()

        password = args.password
        if not password and host not in ("localhost", "127.0.0.1"):
            password = getpass("SMTP Password / App Password: ")

        config = {
            "host": host,
            "port": port,
            "sender": sender,
            "recipient": recipient,
            "password": password,
            "count": args.count,
            "delay": args.delay,
            "concurrency": max(1, args.concurrency),
            "use_tls": use_tls,
            "use_ssl": use_ssl,
            "subject": args.subject,
            "body": "Automated performance benchmark message generated by SMTP Stress Bench.",
            "is_html": args.html,
        }

    print("\n" + "=" * 65)
    print("           INITIALIZING SMTP LOAD TEST BENCHMARK")
    print("=" * 65)
    print(f" Target Server : {config['host']}:{config['port']} (SSL: {config['use_ssl']}, TLS: {config['use_tls']})")
    print(f" Sender        : {config['sender']}")
    print(f" Recipient     : {config['recipient']}")
    print(f" Total Emails  : {config['count']}")
    print(f" Concurrency   : {config['concurrency']} worker(s)")
    print(f" Sleep Delay   : {config['delay']} sec")
    print("=" * 65 + "\n")

    metrics = BenchmarkMetrics(config["count"])
    metrics.start()

    concurrency = config["concurrency"]
    total_count = config["count"]
    per_worker = total_count // concurrency
    remainder = total_count % concurrency

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = []
            for w in range(concurrency):
                worker_iterations = per_worker + (1 if w < remainder else 0)
                if worker_iterations <= 0:
                    continue
                fut = executor.submit(
                    worker_send_task,
                    worker_id=w + 1,
                    iterations=worker_iterations,
                    delay=config["delay"],
                    config=config,
                    metrics=metrics
                )
                futures.append(fut)

            concurrent.futures.wait(futures)

    except KeyboardInterrupt:
        print("\n\n [!] Benchmark interrupted by user (Ctrl+C). Compiling report...")
    finally:
        metrics.stop()
        metrics.print_summary()


if __name__ == "__main__":
    main()
