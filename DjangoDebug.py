from starting import *
import shodan
import requests,re
import os
shodan_API_key = "ENTER_YOUR_SHODAN_API_KEY" #enter your shodan API key
api = shodan.Shodan(shodan_API_key) 
words = open("bug-bounty-wordlist.txt","r")
django_debug_list = open("django-debug-list.txt","w")
for word in words.readlines():
    query = "html:'URLconf defined' ssl:"+word.strip('\n')
    try:
        results = api.search(query)
        print(f"Result found: {results['total']}")
        for result in results['matches']:
            print(word)
            print(f"IP: {result['ip_str']}")
            port = result['port']
            if port in [80,443]:
                if port==443:
                    ip = "https://"+result['ip_str']
                else:
                    ip = "http://"+result['ip_str']
            else:
                ip = "http://"+result['ip_str']+":"+str(port)
            django_debug_list.write(ip+'\n')
            print('')
    except Exception as e:
        print(e)

#automating IP address check

django_debug_list = open("django-debug-list.txt","w")
filesize = os.path.getsize("django-debug-list.txt")
if filesize == 0:
    print("The file is empty: " + str(filesize))#check if file is empty
else:
    regex = r"(?mongodb|redis):\/\/"
    for ip in django_debug_list.readlines():
        try:

            response = requests.post(url=ip.strip("\n")+"/admin",data={},verify=False)
            if re.search(regex,response.content):
                print("mongodb/redis URL Found")

        except Exception as e:
            print(e)