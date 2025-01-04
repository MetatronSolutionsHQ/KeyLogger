
import platform
import socket
from datetime import datetime
import psutil
import requests
from uuid import getnode as get_mac

def get_system_info():
    """
    Gathers and prints system, network, and hardware information.
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

    # # Public IP (v6)
    # try:
    #     public_ip_v6 = requests.get('https://api6.ipify.org', timeout=10).text.strip()
    # except requests.exceptions.RequestException as e:
    #     public_ip_v6 = "Unavailable"
    #     print(f"Error fetching public IP: {e}")

    # Geolocation information for public IP
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
        # vpn_response = requests.get('http://ip-api.com/json?fields=proxy', timeout=5).json()
        # proxy = vpn_response.get('proxy', "Unavailable")
    except requests.exceptions.RequestException as e:
        proxy = "Unavailable"
        print(f"Error fetching vpn_response status: {e}")

    # MAC Address
    mac_address = get_mac()

    # Hardware info
    cpu_freq = psutil.cpu_freq()
    virtual_mem = psutil.virtual_memory()
    disk_partitions = psutil.disk_partitions()

    # Display collected information
    print("========== System Information ==========")
    print(f"System: {uname.system}, Node: {uname.node}, Processor: {uname.processor}")
    print(f"Boot Time: {boot_time}")
    print(f"Local IP: {local_ip}")
    print(f"Public IP: {public_ip}")
    # print(f"Public IP (v6): {public_ip_v6}")
    print(f"IP Details: {ip}, City: {city}, Region: {region}, Postal: {postal}")
    print(f"Timezone: {timezone}, Currency: {currency}, Calling Code: {callcode}, Country: {country}")
    print(f"MAC Address: {mac_address}")
    print(f"VPN Status: {'Using VPN/Proxy' if proxy else 'Not Using VPN/Proxy'}")
    print(f"CPU Frequency: {cpu_freq.max:.2f} MHz")
    print(f"Total Memory: {virtual_mem.total / 1024 ** 3:.2f} GB")
    print("========== Disk Usage ==========")
    for partition in disk_partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Partition {partition.device}: {usage.percent}% used")
        except PermissionError:
            print(f"Permission denied for {partition.device}")
        except Exception as e:
            print(f"Error retrieving disk usage for {partition.device}: {e}")


if __name__ == "__main__":
    get_system_info()
