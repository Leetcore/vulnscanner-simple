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
    target_path = f"scans/{domain}"

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
        os.system(f"mkdir -p {target_path}/")
    
    # run amass
    os.system(f"amass enum -passive -nolocaldb -d {domain} -o {target_path}/amass.txt")
    os.system(f"echo {domain} >> {target_path}/amass.txt")

    # run nmap
    os.system(f"nmap -sV -v --top-ports 50 -T5 --script=vulscan/vulscan.nse --host-timeout 5m --script-args vulscandb=cve.csv --open -iL {target_path}/amass.txt -oN {target_path}/nmap.txt -oX {target_path}/nmap.xml -oG {target_path}/nmap_grep.txt")

    # get webserver from nmap scan
    with open(f"{target_path}/nmap_grep.txt", "r") as myfile:
        content_array = myfile.readlines()
        webservers: list[str] = []
        for line in content_array:
            if "/open/tcp//http" in line or "/open/tcp//ssl|https" in line:
                host_match = re.search('Host: ([0-9\\.]+)', line)
                if isinstance(host_match, re.Match):
                    host = host_match.group(1)
                    ports = re.findall('(\\d+)/open/tcp//http', line)
                    ports += re.findall('(\\d+)/open/tcp//ssl\\|https', line)
                    for port in ports:
                        webservers.append(f"{host}:{port}")


    with open(f"{target_path}/webserver.txt", "w") as myfile:
        myfile.write("\n".join(webservers))

    for webserver in webservers:
        ip = webserver.split(":")[0]
        port = webserver.split(":")[1]

        # run nikto
        os.system(f"nikto -host {ip} -port {port} -Tuning 23457890abcde -timeout 3 -maxtime 5m -useragent 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' -o {target_path}/nikto.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Amass, Nmap + Nikto Scanner")
    main()