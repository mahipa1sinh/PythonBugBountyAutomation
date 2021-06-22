import requests
import wfuzz
import checkdomains
wordlist = requests.get('https://raw.githubusercontent.com/maurosoria/dirsearch/master/db/dicc.txt')
domains = open("bug-bounty-domains-2.txt","r")
payloads = wfuzz.get_payload(wordlist)
for domain in domains.readlines():
    subdomains = open(domain.rstrip("\n")+"_subdomains.txt","r")
    for subdomain in subdomains.readlines():
        urls = checkdomains.isdomainlive(subdomain.rstrip("\n"))
        if urls:
            for url in urls:
                print("fuzzing "+url)
                try:
                    fuzzer = payloads.fuzz(url=url+"/FUZZ",sc=[200])
                    for result in fuzzer:
                        print(result)
                except:
                    pass