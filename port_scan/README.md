## Network Port Scanner & OS Detector
A flexible Python-based CLI tool to automate Nmap scans. It supports scanning single ports, ranges, or lists of ports from an external file, with automatic CSV logging for security auditing.

# 🚀 Features
1. Service Version Detection: Identifies what software version is running on an open port (using -sV).


2. OS Fingerprinting: Attempts to identify the target's operating system (using -O).


3. Flexible Port Input: Supports single ports, ranges (80-443), or bulk lists from a text file.


4. CSV Export: Appends scan results to a CSV file with headers automatically generated.


5. Error Handling: Gracefully handles missing files and unreachable hosts.

# 📋 Prerequisites
Before running the script, ensure you have the following installed:

Nmap: The script requires the Nmap binary on your system.

Linux:
```bash
sudo apt install nmap
```
Windows:

Download from [nmap](https://nmap.org).

## Python-Nmap Library
For Windows :
```python
pip install python-nmap
```
For Linux :
```bash
sudo apt install python3-nmap
```

Note: OS detection (-O) usually requires root/administrator privileges. Run the script with sudo on Linux/macOS or as Administrator on Windows.

## 🛠 Usage
1. Basic Scan (Default Port 80)
```bash
python scanner.py 192.168.1.1
```
2. Scan a Specific Port or List
```bash
python scanner.py 192.168.1.1 -p 22,80,443
```
3. Scan a Port Range
```bash
python scanner.py 192.168.1.1 -sp 1 -lp 1024
```
4. Scan Ports from a File

Create a ports.txt with one port per line, then run:
```bash
python scanner.py 192.168.1.1 -f ports.txt
```
5. Custom Output File
```bash
python scanner.py 192.168.1.1 -p 80 -o my_report.csv
```
## 📊 Output Format
The script generates a CSV file with the following columns: 
```
| Column | Description |

 | :--- | :--- |

| ip | The target IP address. | 

| name | Common name of the service (e.g., http, ssh). | 

| port | The port number scanned. | 

| os | The detected Operating System family. | 

| product | The software product name (e.g., Apache, OpenSSH). | 

| version | The specific version of the software. |
```
## ⚠️ Disclaimer
This tool is for educational and ethical security testing purposes only. Only scan networks and hosts you have explicit permission to test. Unauthorized scanning can be illegal and may be detected by IDS/IPS systems.
