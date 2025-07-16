
## 📜 License

This project is licensed under the Personal Use License. See the [LICENSE](LICENSE) file for details.

## 📚 Table of Contents

- [🚀 Installation](#-installation)
  - [Using pip](#using-pip)
  - [Using Docker](#using-docker)
- [🛠️ Commands](#%EF%B8%8F-commands)
  - [Create NATS Streams](#create-nats-streams)
  - [Run Message Consumer](#run-message-consumer)
  - [Run Task Scheduler](#run-task-scheduler)

## 🚀 Installation

### Using pip

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source ./.venv/bin/activate
   ```

2. Install dependencies:

   **For development:**
   ```bash
   pip install -e ".[dev]"
   ```

   **For production:**
   ```bash
   pip install -e .
   ```

### Using Docker

1. Build Docker image:

   ```bash
   docker build -t trajectory-cli:latest .
   ```

## 🛠️ Commands

```bash
connect-four create-nats-streams <nats_url>
```

### Get busy slots for your date

```bash
trajectory-cli get-busy-slots --date YYYY-MM-DD
```

### Get free slots for your date

```bash
trajectory-cli get-free-slots --date YYYY-MM-DD
```

### Get free slots for your date

```bash
trajectory-cli is-time-available  --date YYYY-MM-DD --start-time HH:MM --end-time HH:MM
```
