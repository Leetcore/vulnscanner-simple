if [[ "$OSTYPE" == "linux"* ]]; then
    echo "install amass nmap nikto"
    apt install git python3 amass nmap nikto
fi

echo "nmap vulscan script"
if [[ -d "/usr/share/nmap/scripts/" ]]
then
    cd /usr/share/nmap/scripts/
    git clone https://github.com/scipag/vulscan.git
    cd vulscan
    git fetch
    curl https://www.computec.ch/projekte/vulscan/download/cve.csv -o cve.csv
fi

# homebrew version
if [[ -d "/opt/homebrew/Cellar/nmap/7.92/share/nmap/scripts/" ]]
then
    cd /opt/homebrew/Cellar/nmap/7.92/share/nmap/scripts/
    git clone https://github.com/scipag/vulscan.git
    cd vulscan
    git fetch
    curl https://www.computec.ch/projekte/vulscan/download/cve.csv -o cve.csv
fi