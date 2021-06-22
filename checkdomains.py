import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def isdomainlive(domain):
    httpsUrl = "https://"+domain
    httpUrl = "http://"+domain
    urls = []
    try:
        requests.get(httpsUrl+"/robot.txt",timeout=5,verify=False)
        urls.append(httpsUrl)
    except:
        pass
    try:
        requests.get(httpUrl+"/robot.txt",timeout=5,verify=False)
        urls.append(httpUrl)
    except:
        pass
    if urls:
        return urls
    else:
        return False