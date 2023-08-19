import os
import platform
import socket

def get_ip():
    try:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        return IPAddr
    except:
        return "Unable to get IP"

def get_hostname():
    return socket.gethostname()

def get_os_name_version():
    os_name = platform.system()
    os_version = platform.version()
    return os_name, os_version

def get_cpu_info():
    return platform.processor()

def main():
    ip_address = get_ip()
    hostname = get_hostname()
    os_name, os_version = get_os_name_version()
    cpu_info = get_cpu_info()
    num_cores = os.cpu_count()

    print(f"IP Address: {ip_address}")
    print(f"Hostname: {hostname}")
    print(f"Operating System Name: {os_name}")
    print(f"Operating System Version: {os_version}")
    print(f"CPU Information: {cpu_info}")
    print(f"Number of Cores: {num_cores}")

if __name__ == '__main__':
    main()
