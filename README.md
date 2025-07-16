
## 📜 License

This project is licensed under the Personal Use License. See the [LICENSE](LICENSE) file for details.

## 📚 Table of Contents

- [🚀 Installation](#-installation)
  - [Using pip](#using-pip)
  - [Using Docker](#using-docker)
- [🛠️ Commands](#%EF%B8%8F-commands)
  - [Get busy slots](#get-busy-slots)
  - [Get free slots](#get-free-slots)
  - [Is time available](#is-time-avaliable)

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

### Is time available

```bash
trajectory-cli is-time-available  --date YYYY-MM-DD --start-time HH:MM --end-time HH:MM
```
