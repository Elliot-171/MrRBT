import argparse
import nmap
import os
import sys
import csv

def scan_host(ip, ports):
    nm = nmap.PortScanner()
    # Adding arguments for service version and OS detection
    nm.scan(ip, ports, arguments='-sV -O') 
    
    host_infos = []

    if ip not in nm.all_hosts():
        return host_infos

    for protocol in nm[ip].all_protocols():
        lport = nm[ip][protocol].keys()
        for port in lport:
            # Safely get OS info if available
            os_family = "unknown"
            if 'osmatch' in nm[ip] and len(nm[ip]['osmatch']) > 0:
                os_family = nm[ip]['osmatch'][0].get('name', 'unknown')

            host_info = {
                "ip": ip,
                "name": nm[ip][protocol][port].get('name', 'unknown'),
                "port": port,
                "os": os_family,
                'product': nm[ip][protocol][port].get('product', 'unknown'),
                'version': nm[ip][protocol][port].get('version', 'unknown')
            }
            host_infos.append(host_info)
    
    return host_infos # Moved outside the loops

def csv_write(output_file, host_infos):
    f_names = ['ip', 'name', 'port', 'os', 'product', 'version']
    file_exist = os.path.isfile(output_file)
    
    with open(output_file, "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=f_names)
        # Only write header if the file is new
        if not file_exist:
            writer.writeheader()
        
        for info in host_infos:
            writer.writerow(info)

def get_ports_from_file(port_f):
    ports = []
    if not os.path.exists(port_f):
        print(f"Error: File {port_f} not found.")
        return ports
    
    with open(port_f, "r") as f:
        for line in f:
            p = line.strip()
            if p:
                ports.append(p)
    return ports

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description="Scan a single host for open ports.")
parser.add_argument("host", help="The target IP address")
parser.add_argument("-sp", "--startport", help="Starting Port")
parser.add_argument("-lp", "--endport", help="Ending port")
parser.add_argument("-p", "--port", help="Single port or comma-separated ports")
parser.add_argument("-o", "--outputfile", help="Output file", default="scan_results.csv")
parser.add_argument("-f", "--portfile", help="File containing ports")

args = parser.parse_args()

# Determine which ports to scan
target_ports = ""

if args.portfile:
    file_ports = get_ports_from_file(args.portfile)
    target_ports = ",".join(file_ports)
elif args.startport and args.endport:
    target_ports = f"{args.startport}-{args.endport}"
else:
    target_ports = args.port if args.port else "80"

# --- Execution ---
print(f"[*] Scanning {args.host} on ports: {target_ports}")

try:
    results = scan_host(args.host, target_ports)
    
    if results:
        csv_write(args.outputfile, results)
        print(f"\n[+] Scan Complete. Found {len(results)} open ports.")
        print("-" * 30)
        for info in results:
            print(f"PORT: {info['port']} | SERVICE: {info['name']} | VERSION: {info['version']}")
    else:
        print("\n[-] No open ports found or host is down.")

except Exception as e:
    print(f"\n[!] An error occurred: {e}")
