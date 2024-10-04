#!/usr/bin/bash
# Cups
sudo pacman -S --noconfirm --needed cups cups-browsed \
    foomatic-db-engine foomatic-db foomatic-db-ppds foomatic-db-nonfree foomatic-db-nonfree-ppds \
    gutenprint foomatic-db-gutenprint-ppds \
    hplip \
    epson-inkjet-printer-escpr epson-inkjet-printer-escpr2 \
    system-config-printer

# Enable and start Cups
sudo systemctl enable --now cups
sudo systemctl enable --now cups-browsed

# Add user to lp group
sudo usermod -a -G lp $(whoami)