import os
import sys
import time
import signal
from collections import defaultdict
from scapy.all import *

THRESHOLD = 40
packet_count = defaultdict(int)
start_time = [time.time()]
blocked_ips = set()

def log_event(ip, message):
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_file = os.path.join(log_folder, "attack_log.txt")
    with open(log_file, "a") as file:
        file.write(f"[{timestamp}] {ip}: {message}\n")

def cleanup_and_exit(sig=None, frame=None):
    """Removes all iptables rules created during this session."""
    print("\n[!] Shutting down... Cleaning up firewall rules.")
    for ip in list(blocked_ips):
        print(f"[*] Unblocking {ip}...")
        os.system(f"iptables -D INPUT -s {ip} -j DROP")
    
    print("[+] Cleanup complete. Exiting.")
    sys.exit(0)

def packet_callback(packet):
    if IP in packet:
        src_ip = packet[IP].src
        packet_count[src_ip] += 1
        
        current_time = time.time()
        time_interval = current_time - start_time[0]

        if time_interval >= 1:
            for ip, count in list(packet_count.items()):
                packet_rate = count / time_interval
                if packet_rate > THRESHOLD and ip not in blocked_ips:
                    print(f"[*] Blocking IP: {ip} | Rate: {packet_rate:.2f} pkts/sec")
                    os.system(f"iptables -A INPUT -s {ip} -j DROP")
                    blocked_ips.add(ip)
                    log_event(ip, f"Blocked (Rate: {packet_rate:.2f})")

            packet_count.clear()
            start_time[0] = current_time

# Register signal handlers for graceful exit (Ctrl+C and kill commands)
signal.signal(signal.SIGINT, cleanup_and_exit)
signal.signal(signal.SIGTERM, cleanup_and_exit)

if __name__ == "__main__":
    if os.getuid() != 0:
        print("[!] Root privileges (sudo) required!")
        sys.exit(1)

    try:
        print(f"[+] Threshold set to {THRESHOLD}")
        print("[*] Monitoring Traffic... Press Ctrl+C to stop.")
        sniff(filter="ip", prn=packet_callback, store=0)
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    finally:
        # This ensures cleanup happens even if the script crashes
        cleanup_and_exit()
