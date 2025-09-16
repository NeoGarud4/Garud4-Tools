#!/usr/bin/env python3
# Neo Garuda v1.0
# Author: Mr.Seven
# Edukasi / OSINT Toolkit

import requests, socket, os, time
from bs4 import BeautifulSoup
from tabulate import tabulate
from colorama import Fore, init

init(autoreset=True)

# banner (biar bisa diganti gampang aja disini)
banner = """
███▄ ▄███▓▓█████  ▒█████      ▄▄▄▄    ▓█████  █    ██  ▄▄▄       ██▀███  
▓██▒▀█▀ ██▒▓█   ▀ ▒██▒  ██▒   ▓█████▄  ▓█   ▀  ██  ▓██▒▒████▄    ▓██ ▒ ██▒
▓██    ▓██░▒███   ▒██░  ██▒   ▒██▒ ▄██ ▒███   ▓██  ▒██░▒██  ▀█▄  ▓██ ░▄█ ▒
▒██    ▒██ ▒▓█  ▄ ▒██   ██░   ▒██░█▀   ▒▓█  ▄ ▓▓█  ░██░░██▄▄▄▄██ ▒██▀▀█▄  
▒██▒   ░██▒░▒████▒░ ████▓▒░   ░▓█  ▀█▓ ░▒████▒▒▒█████▓  ▓█   ▓██▒░██▓ ▒██▒
"""

# ----------------- FITUR ------------------

def ip_lookup(ip):
    print(Fore.YELLOW + f"[+] Cek lokasi IP: {ip}")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}").json()
        if r.get("status") == "fail":
            print(Fore.RED + "Gagal tracking IP.")
            return
        data = [[k, v] for k, v in r.items()]
        print(tabulate(data, headers=["Field","Value"], tablefmt="fancy_grid"))
    except Exception as e:
        print(Fore.RED + f"Error: {e}")

def scrape(url):
    print(Fore.YELLOW + f"[+] Scraping: {url}")
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text,"html.parser")
        ttl = soup.title.string if soup.title else "-"
        desc = soup.find("meta",attrs={"name":"description"})
        desc = desc["content"] if desc else "-"
        lnks = [a["href"] for a in soup.find_all("a", href=True)[:8]]

        out = [
            ["Title", ttl],
            ["Description", desc],
            ["Links", "\n".join(lnks)]
        ]
        print(tabulate(out, headers=["Data","Value"], tablefmt="grid"))
    except Exception as e:
        print(Fore.RED + f"Gagal scrap: {e}")

def cek_status(url):
    print(Fore.YELLOW + f"[+] Ping ke website {url}")
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            print(Fore.GREEN + f"Website {url} UP (200 OK)")
        else:
            print(Fore.RED + f"Website {url} respon: {res.status_code}")
    except:
        print(Fore.RED + "Website down / timeout")

def domain_ip(dom):
    print(Fore.YELLOW + f"[+] Resolve domain: {dom}")
    try:
        ip = socket.gethostbyname(dom)
        print(Fore.CYAN + f"{dom} -> {ip}")
    except:
        print(Fore.RED + "Gagal resolve domain.")

def reverse_ip(ip):
    print(Fore.YELLOW + f"[+] Reverse IP {ip}")
    try:
        r = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}")
        if "error" in r.text.lower():
            print(Fore.RED + "Tidak ada hasil")
        else:
            print(r.text)
    except:
        print(Fore.RED + "Error koneksi")

def header_info(url):
    print(Fore.YELLOW + f"[+] Ambil headers {url}")
    try:
        r = requests.get(url, timeout=5)
        hdrs = [[k,v] for k,v in r.headers.items()]
        print(tabulate(hdrs, headers=["Header","Value"], tablefmt="fancy_grid"))
    except:
        print(Fore.RED + "Gagal ambil header")

# ----------------- MENU -------------------

def menu():
    os.system("cls" if os.name=="nt" else "clear")
    print(Fore.CYAN + banner)
    print(Fore.MAGENTA + "Neo Garuda v1.0")
    print(Fore.YELLOW + """
[1] IP Tracker
[2] Web Scraper
[3] Cek Website Status
[4] Domain -> IP
[5] Reverse IP Lookup
[6] HTTP Headers Grabber
[0] Exit
""")

if __name__=="__main__":
    while True:
        menu()
        ch = input(Fore.CYAN + ">> Pilih: ")
        if ch=="1":
            ip_lookup(input("IP: "))
        elif ch=="2":
            scrape(input("URL: "))
        elif ch=="3":
            cek_status(input("URL: "))
        elif ch=="4":
            domain_ip(input("Domain: "))
        elif ch=="5":
            reverse_ip(input("IP: "))
        elif ch=="6":
            header_info(input("URL: "))
        elif ch=="0":
            print("Bye!")
            break
        else:
            print("Pilihan salah")
        input("\nEnter untuk lanjut...")
