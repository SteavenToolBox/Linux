#!/usr/bin/bash

sudo pacman-key --keyserver keyserver.ubuntu.com --recv-keys F3B607488DB35A47 3056513887B78AEB
sudo pacman-key --lsign-key F3B607488DB35A47 3056513887B78AEB
sudo pacman -U --noconfirm --needed 'https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-keyring-20240331-1-any.pkg.tar.zst' \
'https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-mirrorlist-18-1-any.pkg.tar.zst' \
'https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-v3-mirrorlist-18-1-any.pkg.tar.zst' \
'https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-v4-mirrorlist-6-1-any.pkg.tar.zst' \
'https://mirror.cachyos.org/repo/x86_64/cachyos/pacman-7.0.0.r3.gf3211df-2-x86_64.pkg.tar.zst' \
'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' \
'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'

sudo pacman -S --noconfirm --needed wget


# Set the base backup filename
backup_base="/etc/pacman.conf.backup"
backup_count=1

# Check for existing backups and increment the count
while [ -f "${backup_base}${backup_count}" ]; do
    backup_count=$((backup_count + 1))
done

# Create the backup with the incremented number
sudo mv /etc/pacman.conf "${backup_base}${backup_count}"
echo "Backup created: ${backup_base}${backup_count}"

sudo wget https://github.com/SteavenToolBox/Linux/raw/refs/heads/main/files/arch/pacman.conf -O /etc/pacman.conf