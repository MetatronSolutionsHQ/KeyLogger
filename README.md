# META SNIFFER - Python Security Tools

This repository contains Python-based tools for educational and informational purposes. These scripts are not intended for malicious use. Please use responsibly.  

---

## Contents  

1. **Chrome Password Extractor**  
2. **Keylogger with Discord Integration**  
3. **System Information Checker**  

---

### 1. Chrome Password Extractor  

This script extracts saved passwords from Google Chrome's local storage.  

**Features:**  
- Decrypts Chrome passwords using Windows DPAPI and AES-GCM encryption.  
- Saves extracted data to a local file.  

**Usage:**  
1. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script:
   ```bash
   python ChromeSniffer.py
   ```
3. Extracted passwords are saved to `C:\ProgramData\passwords.txt.`

---
### 2. Keylogger

This script logs keystrokes and sends them to a Discord channel via a webhook.

**Features:**  
- Captures keystrokes, including special keys.
- Sends keystroke logs to a specified Discord webhook.

**Usage:**  
1. Set the Discord Webhook URL in the script:
   ```
   discord_webhook_url = "YOUR_DISCORD_WEBHOOK_URL"
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python Keylogger.py
   ```
---

### 3. A Simple System Information Checker

This script gathers detailed system, network, and hardware information.

**Features:**  
- Collects OS, IP, geolocation, VPN status, CPU, memory, and disk usage.
- Displays information for troubleshooting or educational analysis.

**Usage:**  
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script:
   ```bash
   python SysinfoSniffer.py
   ```

---
## Requirements
Ensure you have Python 3.7+ installed. Install dependencies using:
```bash
pip install -r requirements.txt
```
### Dependencies include:
- `cryptography`
- `pynput`
- `requests`
- `psutil`

---
## Dislaimer
```
These tools are strictly for educational purposes. Unauthorized use, distribution, or deployment for illegal activities is prohibited. Metatron Solutions is not responsible for misuse of the provided scripts. Always adhere to applicable laws and ethical guidelines.
```