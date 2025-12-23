# 🛡️ Sentinel: Real-Time Dynamic Firewall
firewall_sim.py is a lightweight security utility designed to protect Linux systems from packet floods. By leveraging the Scapy library for packet inspection and iptables for enforcement, it provides an automated layer of defense against volumetric network attacks.

## ✨ Key Features
1. Real-Time Traffic Analysis: Sniffs IP traffic to calculate packet-per-second (PPS) rates for every source IP.

2. Automated Mitigation: Automatically injects DROP rules into the Linux kernel firewall when a threshold is exceeded.

3. Graceful Cleanup: Automatically flushes the temporary blocklist and restores iptables states upon script exit (Ctrl+C).

4. Incident Logging: Records every blocking event with timestamps and rate data in logs/attack_log.txt.

5. Safety First: Includes a root-privilege check to ensure the script has the necessary permissions to modify firewall rules.

## ⚙️ How It Works
1. Monitor: The script uses sniff() to capture incoming IP packets.

2. Analyze: It maintains a counter of packets received per source IP within a 1-second window.

3. Threshold Check: If an IP sends more than 40 packets/sec (default), it is flagged as a threat.

4. Block: The script executes: iptables -A INPUT -s [IP] -j DROP.

5. Log: The event is saved to the local log folder for later forensic analysis.

## 🛠️ Installation & Setup
1. Requirements :

Linux OS (Requires iptables).

Python 3.x.

Scapy Library

```bash
pip install scapy
```
2. Execution :

Because the script interacts with the network stack and iptables, it must be run with root privileges:
```bash
sudo python3 firewall_sim.py
```
## 📋 Configuration
You can customize the sensitivity of the firewall by modifying the variables at the top of firewall_sim.py:

Variable	Default	Description :

THRESHOLD	40 --->	Max packets per second allowed before a block is triggered.

log_folder	-----> "logs"	Directory where attack logs are stored.


## ⚠️ Important Considerations
False Positives: A threshold of 40 pkts/sec is relatively low. Legitimate high-traffic applications (like video streaming or heavy file transfers) might be accidentally blocked. Adjust the THRESHOLD based on your typical network environment.

Environment: This script is intended for Linux environments. It will not work on Windows or macOS as they do not use iptables.

Testing: Only use this tool on networks you own or have permission to test.

## 🤝 Contributing
Contributions are welcome! If you'd like to improve the detection logic or add support for nftables, feel free to submit a Pull Request.
