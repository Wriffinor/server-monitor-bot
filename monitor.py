import os
import datetime
import requests
import time

from config import TOKEN, CHAT_ID
SERVERS = ["google.com", "8.8.8.8", "thissitedoesntwork.com"]
LOG_FILE = "/home/wriffinor/projects/monitor/network_log.txt"
BASE_PATH = "/home/wriffinor/projects/monitor/"

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Telegram API error: {response.text}")
    except Exception as e:
        print(f"Network error when sending: {e}")

def check_server(server):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = os.system(f"ping -c 1 {server} > /dev/null 2>&1")
    flag_file = f"{BASE_PATH}{server}_down.txt"

    if response == 0:
        if os.path.exists(flag_file):
            handle_recovery(server, flag_file, current_time)
        return "UP"
    else:
        if not os.path.exists(flag_file):
            handle_failure(server, flag_file, current_time)
        return "DOWN"

def handle_recovery(server, flag_file, current_time):
    try:
        with open(flag_file, "r") as f:
            content = f.read().strip()
        
        if content:
            down_time = float(content)
            duration = round((time.time() - down_time) / 60)
            msg = f"Server {server} RESTORED. Downtime: ~{duration} min. Time: {current_time}"
        else:
            msg = f"Server {server} RESTORED. Time: {current_time}"
            
        send_telegram_msg(msg)
    finally:
        if os.path.exists(flag_file):
            os.remove(flag_file)

def handle_failure(server, flag_file, current_time):

    send_telegram_msg(f"Attention! Server {server} is DOWN. Time: {current_time}")
    with open(flag_file, "w") as f:
        f.write(str(time.time()))

if __name__ == "__main__":
    current_formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Monitoring started at: {current_formatted_time}")
    
    for srv in SERVERS:
        status = check_server(srv)
        with open(LOG_FILE, "a") as log:
            log.write(f"{current_formatted_time} | {srv} | {status}\n")
            
    print("Verification completed.")