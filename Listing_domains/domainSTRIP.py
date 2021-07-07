domains = open("textFiles/bug-bounty-domains.txt","r")
domains2 = open("textFiles/bug-bounty-domains-2.txt","w")
for domain in domains.readlines():
    domains2.write(domain.lstrip('www.'))
