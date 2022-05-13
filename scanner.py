from shlex import quote
import os
import argparse
import re

def main():
    # ask for target domain
    print("Target domain:")
    domain = input()
    start_scanner(domain)

def start_scanner(domain: str):
    domain = quote(domain.strip().lower())
    target_path = f"scans/{domain}/"

    # domain validation
    is_domain = re.fullmatch(
        "^(?!-)[A-Za-z0-9-]+([\\-\\.]{1}[a-z0-9]+)*\\.[A-Za-z]{2,20}$", domain
    )
    if not is_domain:
        print("Invalid domain")
        return

    # Add a pretty banner
    print(
        """
/..---..---..---..---..----..---. .---.
||  -||  -||'-/ /| |  | || || |-< | |- 
--'---''---' '-' '---''----''-''-''---'
Amass + Nmap + Nikto Automatisierung von 1337core
	"""
    )

    # check if folder exists already
    if os.path.exists(target_path) == True:
        print(f"[-] Path in {target_path} already exist!")
    else:
        os.system(f"mkdir -p {target_path}")
    
    # run amass
    os.system(f"amass enum -max-dns-queries 20 -w dns.txt -d {domain} -o {target_path}amass.txt")

    # run nmap
    os.system(f"nmap -A -v -Pn --top-ports 1337 --script vulners -T4 --host-timeout 5m --open -iL {target_path}amass.txt -oN {target_path}nmap.txt -oX {target_path}nmap.xml")

    # run nikto
    os.system(f"cat {target_path}amass.txt | nikto -host - -Tuning 23457890abcde -timeout 3 -port 80,443 -maxtime 5m -useragent 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' -o {target_path}nikto.txt")

    # TODO: port -> show service, show script vulners -> cve

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Amass + Nmap Scanner")
    main()