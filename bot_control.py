import telebot
import os
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FILE = os.path.join(BASE_DIR, "servers.txt")

SERVERS = []

def load_servers():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    return []

SERVERS = load_servers()

@bot.message_handler(commands=['list'])
def send_server_list(message):
    if SERVERS:
        response = "*List of monitored servers:*\n\n"
        for i, server in enumerate(SERVERS, 1):
            response += f"{i}. `{server}`\n"
        bot.reply_to(message, response, parse_mode='Markdown') 
    else:
        bot.send_message(message.chat.id, "📭 The server list is empty.")

@bot.message_handler(commands=['status'])
def send_status(message):
    global SERVERS
    SERVERS = load_servers()
    
    if not SERVERS:
        bot.reply_to(message, "No servers to check.")
        return

    report = "*Current Server Statuses:*\n\n"
    for srv in SERVERS:
        response = os.system(f"ping -c 1 {srv} > /dev/null 2>&1")
        status = "UP" if response == 0 else "DOWN"
        report += f"• {srv}: {status}\n"
    
    bot.send_message(message.chat.id, report, parse_mode='Markdown')

@bot.message_handler(commands=['add'])
def add_server(message):
    parts = message.text.split()
    if len(parts) > 1:
        new_server = parts[1].lower()
        if new_server not in SERVERS:
            with open(DB_FILE, "a") as file:
                file.write(new_server + "\n")
            SERVERS.append(new_server)
            bot.reply_to(message, f"Server `{new_server}` added!")
        else:
            bot.reply_to(message, f"`{new_server}` is already in the list.")
    else:
        bot.reply_to(message, "Example: `/add google.com`", parse_mode='Markdown')

@bot.message_handler(commands=['remove'])
def remove_server(message):
    parts = message.text.split()
    if len(parts) > 1:
        target = parts[1].lower()
        if target in SERVERS:
            SERVERS.remove(target)  
            with open(DB_FILE, "w") as file:
                for s in SERVERS:
                    file.write(s + "\n")
            bot.reply_to(message, f"`{target}` has been deleted")    
        else:
            bot.reply_to(message, f"`{target}` not found.")
    else:
        bot.reply_to(message, "Example: `/remove google.com`", parse_mode='Markdown')

print("Bot is starting...")
bot.polling()