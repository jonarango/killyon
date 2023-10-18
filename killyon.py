########################################################
# Original developer: unknown
# Improved and fixed by: https://github.com/ITSXNOOBX
########################################################

import subprocess
import sys
import threading
import ctypes
import time
import os

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from plyer import notification

def block_firewall_port(port):
    rule_name = "Block_Port_" + str(port)
    command = f'New-NetFirewallRule -DisplayName "{rule_name}" -Direction Inbound -Protocol TCP -Action Block -LocalPort {port}'
    subprocess.call(["powershell.exe", "-Command", command])

def unblock_firewall_port(port):
    rule_name = "Block_Port_" + str(port)  # Match the rule name used for blocking
    command = f'Remove-NetFirewallRule -Name "{rule_name}"'
    subprocess.call(["powershell.exe", "-Command", command])

def control_service(stop, servicename):
    command = f"net {'stop' if stop else 'start'} {servicename}"
    subprocess.call(["cmd.exe", "/c", command])

def check_port(port):
    try:
        ps_cmd = f'Get-NetTCPConnection -LocalPort {port} | Select-Object -Property LocalAddress, LocalPort, RemoteAddress, RemotePort, State | Sort-Object LocalPort | Format-Table'
        result = subprocess.check_output(f'powershell.exe "{ps_cmd}"', shell=True)
        if b"Established" in result:
            return port
    except subprocess.CalledProcessError:
        pass

    return None

def check_monitor(ports_to_check=None):
    if not ports_to_check:
        ports_to_check = [11100, 11200]  # Default port to check if none specified

    monitored_ports = []

    threads = []
    for port in ports_to_check:
        t = threading.Thread(target=lambda p=port: monitored_ports.append(check_port(p)))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    monitored_ports = [port for port in monitored_ports if port is not None]
    return monitored_ports

def main():
    is_admin = False
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    if not is_admin:
        print(f"{Fore.LIGHTRED_EX}You need to run this script as administrator.{Style.RESET_ALL}")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    is_notified = False

    while True:
        is_monitored = check_monitor(None)
        if is_monitored:
            notification.notify(
                title = 'KillYon',
                message = 'Someone seems to have started monitoring you.',
                app_icon = None,
                timeout = 5,
            )
            print(f"{Fore.LIGHTRED_EX}Someone seems to have started monitoring you.{Style.RESET_ALL}")
            if 11200 in is_monitored:
                block_firewall_port(11200)
            if 11100 in is_monitored:
                block_firewall_port(11100)
            # control_service(True, "VeyonService")
            is_notified = True
        else:
            print(f"{Fore.GREEN}No Veyon connections detected.{Style.RESET_ALL}")
            if not 11200 in is_monitored:
                unblock_firewall_port(11200)
            if not 11100 in is_monitored:
                unblock_firewall_port(11100)
            # control_service(False, "VeyonService")
            # unblock_firewall_port(11200)
            is_notified = True
        time.sleep(0.1)

if __name__ == "__main__":
    main()
