import telebot
import os

from config import TOKEN
bot = telebot.TeleBot(TOKEN)
SERVERS = ["google.com", "8.8.8.8", "thissitedoesntwork.com"]

@bot.message_handler(commands=['status'])
def send_status(message):
    report = "**Current server status:**\n\n"
    
    for server in SERVERS:
        response = os.system(f"ping -c 1 {server} > /dev/null 2>&1")
        status_icon = "UP" if response == 0 else "DOWN"
        report += f"{server}: {status_icon}\n"
    
    bot.reply_to(message, report, parse_mode='Markdown')
bot.polling()