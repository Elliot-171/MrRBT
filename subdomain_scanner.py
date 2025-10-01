import requests

domain=input("Enter domain :")
file=open("subdomains-1000.txt")
content=file.read()

subdomains=content.splitlines()
d_subdomains=[]

for subdomain in subdomains:
   url=f"http://{subdomain}.{domain}"
   try:
     requests.get(url)
   except requests.ConnectionError:
     pass
     
   else:
     print("[+]Discovered Subdomain:",url)
     
   d_subdomains.append(url)
   
