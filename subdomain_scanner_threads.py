import requests
import threading
import time
domain=input("Enter domain :")
t=time.perf_counter()
file=open("subdomains-1000.txt")
content=file.read()
subdomains=content.splitlines()
def sub_domain(subdomain):
      url=f"http://{subdomain}.{domain}"
      try:
        requests.get(url)
      except requests.ConnectionError:
        pass
      except requests.exceptions.TooManyRedirects:
        print("TOO MANY REDIRECTS...PASSING ON")
      except requests.exceptions.Timeout:
        pass
     
      else:
        print("[+]Discovered Subdomain:",url)
        

threads=[]
stop_event=threading.Event()
for subdomain in subdomains:
    thread_daemon=threading.Thread(target=sub_domain,name="subdomain",args=(subdomain,))
    thread_daemon.setDaemon(True)
    threads.append(thread_daemon)
for thread in threads:
    thread.start()
    
for thread in threads:
    thread.join(timeout=2.5)
stop_event.set()
ti=time.perf_counter()
print(f"{(ti-t)/1000:.9f}s")

   
