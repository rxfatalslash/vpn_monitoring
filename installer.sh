#!/bin/bash

# Variables de color
CRE=$(tput setaf 1)
CGR=$(tput setaf 2)
CYE=$(tput setaf 3)
CBL=$(tput setaf 4)
BLD=$(tput bold)
CNC=$(tput sgr0)

# Logo
logo () {

    local text="${1:?}"
    echo -en "
    WOdddddxk0KNW                                            WNK0kxdddddOW 
     Wo........',:lx0N                                    N0xl:,'........oW 
      Xc.,clcc:;'....;lON                              NOl;....';:cclc,.cX  
       Kc'cdodlc::ccc;..:kN                          Nk:..;ccc::cldodc'cK   
        Xo;:loooooooool:,'cK                        Kc',:loooooooool:;oX    
         WKxolccclllllllc;';OW                    WO;';clllllllcccloxKW     
            WNKOOOOkkkOkkkdokN                    NkodkkkOkkkOOOOKNW       
    \n\n"
    printf ' %s [%s%s %s%s %s]%s\n\n' "${CRE}" "${CNC}" "${CYE}" "${text}" "${CNC}" "${CRE}" "${CNC}"
}

logo "rxfatalslash"

if [ "$(whoami)" != root ]; then
    printf "%s%s[ERROR] El script debe ejecutarse como root%s\n\n" "${BLD}" "${CRE}" "${CNC}"
    exit 0
fi

printf "%s%s[+] Iniciando proceso de instalación...%s\n\n" "${BLD}" "${CRE}" "${CNC}"

# Confirmación
while true; do
    read -rp "¿Quieres continuar con la instalación [s/N]: " confirm
    case $confirm in
        [Ss]*) break;;
        [Nn]*) exit;;
        *) printf "%s%s[ERROR] Escribe solo 's' o 'n'%s\n\n" "${BLD}" "${CRE}" "${CNC}"
    esac
done

# Instalación Python 3
sudo apt-get update -y && apt-get upgrade -y

clear
logo "[+] Instalando Python..."
sudo apt-get install python3
sudo apt-get install python3-pip

clear
logo "[+] Copiando archivos y habilitando servicios..."
pip3 install -r requirements.txt
chmod +x vpn_monitoring.py vpn_alert.service
sudo cp vpn_monitoring.py /usr/bin
sudo cp vpn_alert.service /lib/systemd/system
sudo ln -s /lib/systemd/system/vpn_alert.service /etc/systemd/system/vpn_alert.service

sudo systemctl daemon-reload
sudo systemctl enable vpn_alert.service
sudo systemctl start vpn_alert.service