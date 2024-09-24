#!/usr/bin/bash
# Cups
sudo dnf install -y cups \
    foomatic-db foomatic-db-ppds \
    gutenprint \
    hplip \
    epson-inkjet-printer-escpr epson-inkjet-printer-escpr2 \
    system-config-printer

# Enable and start Cups
sudo systemctl enable --now cups

# Add user to lp group
sudo usermod -a -G lp $(whoami)