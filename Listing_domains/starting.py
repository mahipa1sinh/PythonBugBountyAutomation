from bs4 import BeautifulSoup as sp
import requests
import tldextract
url = "https://www.vulnerability-lab.com/list-of-bug-bounty-programs.php"
try:
    webpage = requests.get(url=url) #send a get request
     
    soup = sp(webpage.content,"html.parser")
    tables = soup.find_all('table')
    a_tags = tables[4].find_all('a')
    sites_list = open("textFiles/bug-bounty-sites.txt","w")
    for a in a_tags:
        sites_list.write(a.get('href')+'\n')
except Exception as e:
    print(TimeoutError)

#next step is to sanitize the sites to get domain names without scheme and path

sites_list = open("textFiles/bug-bounty-sites.txt",'r')
sites = sites_list.readlines()
domain_list = open("textFiles/bug-bounty-domains.txt","w")
for site in sites:
    if not 'mailto' in site:
        split_site = site.split('/')
        if len(split_site)>1:
            domain_list.write(split_site[2]+'\n')

#getting keyword list from domain list

#domain_list = open("bug-bounty-domains.txt","r")
#word_list = open("bug-bounty-wordlist.txt","w")
#for domain in domain_list.readlines():
#    split_domain = domain.split(".")
#    if len(split_domain)>1:
#        if len(split_domain[-2])>2:
#            word_list.write(split_domain[-2]+"\n")

#above code havs some issues
#there is another way

domain_list = open("textFiles/bug-bounty-domains.txt","r")
word_list = open("textFiles/bug-bounty-wordlist.txt","w")
for domain in domain_list.readlines():
    tld = tldextract.extract(domain)
    word_list.write(tld.domain+"\n")

#