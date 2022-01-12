import sys
import requests

def print_to_txt(message, file, BOT_TOKEN, CHAT_ID):
    print(message)

    original_stdout = sys.stdout # Save a reference to the original standard output

    with open(file, 'a') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print(message)
        sys.stdout = original_stdout # Reset the standard output to its original value
    
    f.close()

    # Send message to telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = { "chat_id": CHAT_ID, "text": message }
    requests.get(url, params=params)