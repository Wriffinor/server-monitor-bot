# 🛡️ Server Monitor Telegram Bot

## 🚀 Key features
* **Autonomous monitoring**: Runs in the background, checking nodes every minute.
* **Downtime analytics**: Automatically calculates the duration of server unavailability (in minutes) when it is restored.
* **Smart notifications**: The bot sends notifications only when the status changes (Up -> Down or Down -> Up), avoiding spam.
* **Interactive control**: Get the current status of all servers on demand using the `/status` command.

## 🛠️ Technologies and environment
* **Language**: Python 3.12.
* **OS**: Linux (Ubuntu 24.04).
* **Process management**: Bash scripting for stable startup and background task management.
* **Infrastructure**: Virtual environment (`venv`) for dependency isolation.

## 📂 Project structure
* `monitor.py` — main script for checking and logging.
* `bot_control.py` — interactive bot for processing `/status` commands.
* `start_system.sh` — startup manager that controls background processes.
* `config.py` — configuration file with tokens (protected by `.gitignore`).
* `network_log.txt` — history of server statuses.
* `bot.log` — technical log of the Telegram bot's operation.

## ⚙️ Installation and launch

1. **Environment setup**:
* bash
* python3 -m venv venv
* source venv/bin/activate
* pip install pyTelegramBotAPI requests

2. **Configuration: Create a config.py file and add your data:**
 * TOKEN = “your_token”
 * CHAT_ID = “your_id”

3. **System launch: Use an automated script for safe launch without process conflicts:**
 * chmod +x start_system.sh
 * ./start_system.sh

## ⏲️ Automation (Scheduling)
To ensure the monitoring script runs autonomously every minute, you need to set up a `cron` job:

1. **Open the crontab editor:**
  * " ```bash "
   * crontab -e
2. **Add the following line (use absolute paths):**
  " * * * * * /home/user_name/projects/monitor/venv/bin/python3 /home/user_name/projects/monitor/monitor.py >> /home/user_name/projects/monitor/cron_errors.log 2>&1 "

## 📊 Test results

 * The bot demonstrated high performance, successfully recording and processing node recovery periods with correct timestamp preservation.