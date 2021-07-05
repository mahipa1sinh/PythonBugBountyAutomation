import re
import shodan
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import chromedriver_binary

API_key_shodan = "ENTER_YOUR_SHODAN_API_KEY" #your shodan api key goes here
api = shodan.Shodan(API_key_shodan)
out_file = open('jenkins-instances.txt','a')
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

options = Options()
options.headless = False
username = "Mahipalsinhnakum"
password = "mAHI@01022002"
jenkins_list = open('jenkins-instances.txt','r').readlines()
for jenkins in jenkins_list:
    jenkins = jenkins.rstrip('\n')
    print('Checking- '+jenkins)
    #options.binary_location = r'C:/Program Files/Google/Chrome/Application/Chrome'
    driver = webdriver.Chrome(options=options,executable_path='C:/Program Files/chromedriver.exe')
    driver.set_page_load_timeout(20)
    try:
        driver.get(jenkins)
    except:
        print("Page load timeout")
    driver.implicitly_wait(20)
    try:
        element = driver.find_element_by_id('login_field')
        element.send_keys(username)
        element = driver.find_element_by_id('password')
        element.send_Keys(password)
        element = driver.find_element_by_name('commit')
        element.click()
        element = driver.find_element_by_id('js-oauth-authorize-btn')
        element.click()
    except:
        pass
    if re.findall(r'Manage\sJenkins',driver.page_source):
        print(jenkins+'-Jenkins Misconfigured')

