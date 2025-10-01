import dns.resolver

target_domain=input("Enter domain:")
record_types=["A","AAAA","CNAME","MX","NS","SOA","TXT"]

resolver=dns.resolver.Resolver()

for record_type in record_types:
  try:
    answers=resolver.resolve(target_domain,record_type)
  except dns.resolver.NoAnswer:
    continue
    
  print(f"{record_type} records for {target_domain}:")
  for r_data in answers:
    print(f"{r_data}")
    
