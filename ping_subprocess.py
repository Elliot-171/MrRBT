import subprocess
import socket

ch=input("Enter h to input host name or Enter i to enter ip address(IPv4) :")
try:
 if ch=='i':
  ip=input("Enter ip :")
  result=subprocess.run(["ping",ip])
  print(result)
 elif ch=='h':
  h=input("Enter host website (ex:example.com):")
  ip_addr=socket.gethostbyname(h)
  result=subprocess.run(["ping",ip_addr])
  print(result)

 else:
  print("Invalid Input !")
  
except KeyboardInterrupt:
 print("CTRL-C Detected ! Exiting...")
 

  

  
