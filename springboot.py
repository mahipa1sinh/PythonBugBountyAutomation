import requests
import shodan
import wfuzz
API_key_shodan = "ENTER_YOUR_SHODAN_API_KEY" #your shodan api key goes here
api = shodan.Shodan(API_key_shodan)
out_file = open('spring-boot-server.txt','a')
query = 'http.favicon.hash:116323821'
try:
    results = api.search(query)
    print(f"Results found: {results['total']}")
    for result in results['matches']:
        print(f"IP: {result['ip_str']}"+':'+str(result['port']))
        if result['port'] in [80,443]:
            if result['port']==80:
                scheme = "http://"
            else:
                scheme = "https://"
            out = scheme+result['ip_str']
        else:
            out = "http://"+result['ip_str']+':'+str(result['port'])
        out_file.write(out+'\n')
except shodan.APIError as e:
    print(f"Error: {e}")

#fuzzing IP

wordlist = requests.get('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/WebContent/spring-boot.txt').text.split("\n")
springs = open("spring-boot-servers.txt","r")
payloads = wfuzz.get_payload(wordlist)
for spring in springs.readlines():
    print("Fuzzing - "+spring)
    try:
        fuzzer = payloads.fuzz(url=spring.rstrip("\n")+"/FUZZ",sc=[200])
        for result in fuzzer:
            print(result)
    except:
        pass