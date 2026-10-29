# SMTP Stress Bench

<p align="center">
  <strong>High-Performance Mail Server Load Testing & Resilience Benchmarking Suite</strong>
</p>

<p align="center">
  <a href="https://github.com/SagarBiswas-MultiHAT/EmailBomber/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-GPL%20v3-blue.svg?style=flat-square" alt="License: GPL v3"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square" alt="Python Version"></a>
  <a href="https://github.com/SagarBiswas-MultiHAT/EmailBomber/stargazers"><img src="https://img.shields.io/github/stars/SagarBiswas-MultiHAT/EmailBomber?style=flat-square" alt="GitHub Stars"></a>
  <a href="https://github.com/SagarBiswas-MultiHAT/EmailBomber/network/members"><img src="https://img.shields.io/github/forks/SagarBiswas-MultiHAT/EmailBomber?style=flat-square" alt="GitHub Forks"></a>
  <a href="https://github.com/SagarBiswas-MultiHAT/EmailBomber/issues"><img src="https://img.shields.io/github/issues/SagarBiswas-MultiHAT/EmailBomber?style=flat-square" alt="Issues"></a>
  <a href="https://github.com/SagarBiswas-MultiHAT/EmailBomber/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome"></a>
</p>

---

## Overview

**SMTP Stress Bench** is a lightweight, multi-threaded command-line benchmarking tool designed for DevOps engineers, system administrators, and backend developers. It provides controlled email throughput generation to evaluate mail server capacity, latency, queue resilience, and rate limits in local and staging environments.

Whether you are validating an internal mail relay, tuning a Postfix or Exim server, or load-testing local development mock servers like Mailpit and MailHog, SMTP Stress Bench gives you real-time metrics and latency tracking with zero external dependencies.

```text
=================================================================
                 SMTP BENCHMARK SUMMARY REPORT
=================================================================
 Total Requests Scheduled : 100
 Successful Deliveries    : 100 (100.0%)
 Failed Deliveries        : 0
 Total Elapsed Time       : 4.82 seconds
 Effective Throughput     : 20.75 emails/sec
-----------------------------------------------------------------
 Min Latency              : 18.40 ms
 Avg Latency              : 32.15 ms
 Max Latency              : 64.10 ms
=================================================================
```

---

## Key Features

- **Zero External Dependencies:** Built entirely on Python 3 standard libraries (`smtplib`, `concurrent.futures`, `argparse`). Runs out of the box anywhere Python is installed.
- **Concurrent Load Generation:** Configurable worker threads to test multi-connection throughput and server connection pooling.
- **Precision Latency Tracking:** Measures per-request response times, calculating minimum, average, and maximum delivery latency in milliseconds.
- **Comprehensive Failure Analysis:** Automatically captures, classifies, and reports authentication failures, connection resets, and server timeouts.
- **Multi-Protocol Support:**
  - Standard SMTP (Port 25, 587, 1025)
  - Opportunistic TLS (STARTTLS)
  - Direct SSL/TLS encryption (Port 465)
- **Interactive Wizard or Headless CLI:** Run interactively with step-by-step prompts, or pass CLI flags for automated CI/CD load testing.
- **Payload Customization:** Supports both lightweight plaintext benchmarking payloads and rich multipart HTML templates.
- **Graceful Interruption:** Pressing `Ctrl+C` halts ongoing workers safely and generates a complete report of all completed iterations up to that moment.

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/SagarBiswas-MultiHAT/EmailBomber.git
cd EmailBomber
```

### 2. Run the Interactive Wizard

If you run without arguments, the tool automatically launches the interactive wizard:

```bash
python main.py
```

### 3. Run via Command-Line Flags

```bash
# Benchmark local Mailpit or MailHog test server (port 1025, unencrypted)
python main.py -H localhost -P 1025 -s test@example.com -r inbox@example.com -n 50 -c 4 --no-tls

# Benchmark remote staging SMTP server with STARTTLS and 0.2s delay
python main.py -H smtp.gmail.com -P 587 -s your_email@gmail.com -p "your_app_password" -r test_inbox@example.com -n 20 -d 0.2
```

---

## CLI Options and Flags

| Flag | Short | Environment Variable | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--host` | `-H` | `SMTP_HOST` | `smtp.gmail.com` | Target SMTP server hostname or IP address |
| `--port` | `-P` | `SMTP_PORT` | `587` | Target port (587 for TLS, 465 for SSL, 25/1025 for plain) |
| `--sender` | `-s` | `SMTP_USER` | None | Sender email address |
| `--recipient` | `-r` | None | None | Target recipient or test inbox address |
| `--password` | `-p` | `SMTP_PASSWORD` | None | Authentication password or Gmail App Password |
| `--count` | `-n` | None | `10` | Total number of test emails to dispatch |
| `--concurrency` | `-c` | None | `1` | Number of concurrent worker threads |
| `--delay` | `-d` | None | `0.5` | Delay in seconds between sends per worker |
| `--ssl` | None | None | `False` | Use direct SSL connection (typically port 465) |
| `--no-tls` | None | None | `False` | Disable STARTTLS (for unencrypted local test servers) |
| `--subject` | None | None | `"SMTP Benchmark Test Message"` | Custom subject line |
| `--html` | None | None | `False` | Send multipart HTML payload instead of plain text |
| `--interactive` | `-i` | None | `False` | Force interactive step-by-step wizard mode |

---

## Common Benchmarking Recipes

### Testing Local Development Mail Servers (Mailpit / MailHog)

Mock servers are ideal for high-volume stress testing without triggering public email service rate limits:

```bash
python main.py -H 127.0.0.1 -P 1025 -s bench@test.local -r target@test.local -n 200 -c 5 -d 0.05 --no-tls
```

### Testing Staging SMTP Server with HTML Payloads

Measure server throughput when handling heavier MIME multipart HTML bodies:

```bash
python main.py -H mail.staging.example.com -P 587 -s dev@example.com -p "secret123" -r test@example.com -n 50 -c 2 --html
```

---

## Environment Variables Configuration

To run tests without typing credentials in the terminal, copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Define your settings:

```ini
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

The tool will read these environment variables automatically whenever matching CLI flags are omitted.

---

## Intellectual Property & License Protection

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

- **Copyright (C) 2026 Sagar Biswas. All rights reserved.**
- Under the terms of the GPL-3.0, you are free to inspect, run, modify, and distribute this software.
- Any derivative works, forks, or distributed modifications **must** also remain open source under the GPL-3.0 license and preserve full author attribution to Sagar Biswas.
- Closed-source proprietary redistribution or commercial rebranding without source disclosure is strictly prohibited by law.

For full license terms, refer to the [LICENSE](LICENSE) file.

---

## Ethical and Authorized Use

This utility is developed strictly for authorized network resilience verification, system benchmarking, and development debugging. Testing servers without prior authorization from the infrastructure owner is strictly forbidden. The author assumes no liability for misuse. Please review [SECURITY.md](SECURITY.md) for our responsible testing policy.

---

## Contributing and Community

Contributions, feature requests, and bug reports are welcome. Please check [CONTRIBUTING.md](CONTRIBUTING.md) for details on submitting pull requests.

If you find this project helpful, please consider starring the repository to help others discover it.
