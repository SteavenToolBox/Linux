#!/usr/bin/bash

# Cli Apps
sudo dnf install -y 'dnf-command(copr)'
sudo dnf copr enable -y atim/starship 
sudo dnf install -y starship zoxide fastfetch trash-cli bat speedtest-cli neovim vim nano unzip unrar neofetch hyfetch xclip lolcat eza gh flatpak
# missing, topgrade

# Apps that i use
sudo dnf copr enable -y sergiomb/electrons 
sudo dnf copr enable -y andykimpe/notepadqq
sudo dnf install -y discord \
    libreoffice xreader \
    obs-studio obs-studio-plugin-vkcapture \
    gimp kdenlive mediainfo mediainfo-gui \
    qbittorrent \
    firefox vlc audacious
    nemo-mediainfo-tab \
    ente-auth-bin \
    obs-pipewire-audio-capture-bin \
    element-desktop notepadqq
# missing bitwarden whatsie visual-studio-code github-desktop phonon-qt6-mpv gstreamer-vaapi obs-gstreamer freedownloadmanager

# Disks app
sudo dnf install -y gnome-disk-utility gparted \
    dosfstools btrfs-progs ntfs-3g exfatprogs mtools

# Eco System
sudo dnf copr enable -y hazel-bunny/syncthing-unofficial 
sudo dnf install -y openssh syncthing syncthingtray-qt6
sudo systemctl enable --now sshd
sudo systemctl enable --now syncthing@$(whoami)

# Add user to groups
sudo usermod -a -G wheel,audio,disk,input,kvm,lp,render,storage,uucp,video,gamemode,libvirt,power,flatpak $(whoami)