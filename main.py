#!/usr/bin/python3

import random
import concurrent.futures
import string
import requests
import os
import csv
import sys
from bs4 import BeautifulSoup


try:
    os.mkdir("output")
except:
    pass

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def scrape(cap_num):

    proxylist = []

    with open('proxies.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            proxylist.append(row[0])

    proxy = random.choice(proxylist)
    scraped_num = 0
    while cap_num > scraped_num:
        try:
            slug = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            url = "https://prnt.sc/" + slug
            response = requests.get(url, proxies={'https': "socks4://" + proxy,'http': "socks4://" + proxy}, headers=headers, timeout=1)
            content = response.content.decode()
            soup = BeautifulSoup(content, features='lxml')
            ufr = requests.get(soup.img['src'], headers=headers)
            f = open(f'output/{slug}.png', 'wb')
            f.write(ufr.content)
            f.close()
            print(f'[+] Received file {slug}.png')
            scraped_num += 1
        except requests.exceptions.MissingSchema:
            pass
        except:
            pass



def main():
    
    if len(sys.argv) == 2:
            print("[*] Downloading captures from " + str(sys.argv[1]) + " links...")
    else:
        print("[!] Usage: python3 " + sys.argv[0] + " <number of captures you want to download> ")
        sys.exit(1)

    n_of_links = int(sys.argv[1])

    scrape(n_of_links)

if __name__ == "__main__":
    main()
