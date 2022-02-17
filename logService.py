import time
import traceback
import requests

def print_to_txt(message, file):
    print(message)

    with open(file, 'a') as f:
        f.write(message)
        f.write('\n')
    
    f.close()

def send_to_telegram(message, BOT_TOKEN, CHAT_ID):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = { "chat_id": CHAT_ID, "text": message }
    requests.get(url, params=params)

def print_and_send(message, file, BOT_TOKEN, CHAT_ID):
    print_to_txt(message, file)
    send_to_telegram(message, BOT_TOKEN, CHAT_ID)

def error_message_and_delay(e, log_file, delay):
    print_to_txt(f'Exception: {e}', log_file)
    traceback.print_exc()
    print_to_txt("Retrying...", log_file)
    time.sleep(delay) #delay in seconds