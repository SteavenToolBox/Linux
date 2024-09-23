#!/usr/bin/bash

# Cli Apps
sudo pacman -S --noconfirm --needed starship zoxide fastfetch trash-cli bat speedtest-cli neovim vim nano unzip unrar neofetch hyfetch xclip lolcat eza github-cli topgrade

# Apps that i use
sudo pacman -S --noconfirm --needed bitwarden \
    discord whatsie-git element-desktop \
    visual-studio-code-bin github-desktop \
    libreoffice-fresh xreader notepadqq phonon-qt6-mpv \
    obs-studio-stable obs-vkcapture lib32-obs-vkcapture gstreamer-vaapi obs-gstreamer \
    gimp kdenlive mediainfo mediainfo-gui \
    qbittorrent freedownloadmanager \
    firefox vlc audacious
paru -S --noconfirm --needed nemo-mediainfo-tab \
    ente-auth-bin \
    obs-pipewire-audio-capture-bin

# Disks app
sudo pacman -S --noconfirm --needed gnome-disk-utility gparted \
    dosfstools btrfs-progs ntfs-3g exfatprogs mtools

# Eco System
sudo pacman -S --noconfirm --needed openssh syncthing syncthingtray-qt6
sudo systemctl enable --now sshd
sudo systemctl enable --now syncthing@$(whoami)

# Add user to groups
sudo usermod -a -G wheel,audio,disk,input,kvm,lp,render,storage,uucp,video,gamemode,libvirt,power,flatpak $(whoami)