# A Simple System Information Checker

This script gathers detailed system, network, and hardware information.

---
[//]: # ()
[//]: # (## Contents)

[//]: # ()
[//]: # (1. **KeyLogger: Unencrypted**  )

[//]: # ()
[//]: # (2. **Keylogger: Encrypted**  )

[//]: # ()
[//]: # (3. **Decryptor**  )
[//]: # (---)

## Usage
1. Set webhook url in script
2. Install requirements `pip install -r requirements.txt`
3. Compile it using pyinstaller
4. Done
---



## **Features:**  
- Collects OS, IP, geolocation, VPN status, CPU, memory, and disk usage.
- Displays information for troubleshooting or educational analysis.


**APIs/Modules:**  
- `psutil`: For system and hardware information such as CPU and memory.
- `socket` and `requests.get`: For network-related details, including IP and geolocation.
- **External API: ipapi.co** - Fetches geolocation and network details based on public IP.

**Example API Call:**
 ```python
geo_info = requests.get(f'https://ipapi.co/{public_ip}/json').json()
```
- **External API: ipify.org** - Fetches  public IP.

**Example API Call:**
```python
public_ip = requests.get('https://api.ipify.org', timeout=10).text.strip()
```

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

```
WARN: This is for educational purposes only! I do not recommend using it on people!