#!/usr/bin/bash

# Cli Apps
sudo apt install -y zoxide trash-cli bat speedtest-cli neovim vim nano unzip unrar neofetch hyfetch xclip lolcat eza gh
# missing, starship fastfetch topgrade

# Apps that i use
sudo apt install -y libreoffice \
    notepadqq \
    obs-studio \
    gimp kdenlive mediainfo mediainfo-gui \
    qbittorrent \
    firefox vlc audacious 
# missing, bitwarden discord whatsie element-desktop visual-studio-code github-desktop xreader phonon-qt6-mpv obs-vkcapture gstreamer-vaapi obs-gstreamer freedownloadmanager nemo-mediainfo-tab ente-auth obs-pipewire-audio-capture

# Disks app
sudo apt install -y gnome-disk-utility gparted \
    dosfstools btrfs-progs ntfs-3g exfatprogs mtools

# Eco System
sudo apt install -y openssh-client openssh-server openssh-sftp-server syncthing
# missing, syncthingtray-qt6
sudo systemctl enable --now sshd
sudo systemctl enable --now syncthing@$(whoami)

# Add user to groups
sudo usermod -a -G wheel,audio,disk,input,kvm,lp,render,storage,uucp,video,gamemode,libvirt,power,flatpak $(whoami)