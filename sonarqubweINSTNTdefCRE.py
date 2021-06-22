import shodan
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