#!/usr/bin/bash
# Cups
sudo apt install -y cups \
    foomatic-db-engine foomatic-db  \
    hplip \
    system-config-printer
# missing, gutenprint epson-inkjet-printer-escpr epson-inkjet-printer-escpr2

# Enable and start Cups
sudo systemctl enable --now cups

# Add user to lp group
sudo usermod -a -G lp $(whoami)