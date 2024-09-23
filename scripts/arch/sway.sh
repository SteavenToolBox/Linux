#!/usr/bin/bash

# Wayland
sudo pacman -S --noconfirm --needed wayland xorg-xwayland qt5-wayland qt6-wayland wayland-protocols lib32-wayland

# Pipewire
sudo pacman -S --noconfirm --needed pipewire pipewire-jack pipewire-alsa pipewire-pulse \
    lib32-pipewire lib32-pipewire-jack \
    wireplumber pamixer \
    alsa-utils playerctl \
    pavucontrol helvum

# Window manager and its tools
sudo pacman -S --noconfirm --needed sway swayidle swaylock-effects swaync \
    greetd \
    polkit-gnome xdg-desktop-portal xdg-desktop-portal-gtk xdg-desktop-portal-wlr \
    kwallet kwallet-pam kwallet5 kwalletmanager \
    grim grimshot wlsunset \
    waybar rofi-wayland mpv

# Theme and its tools
sudo pacman -S --noconfirm --needed lxappearance qt5ct qt6ct kvantum kvantum-qt5 \
    nordic-theme-git papirus-icon-theme papirus-folders
paru -S --noconfirm --needed whitesur-cursor-theme-git

# Fonts
sudo pacman -S --noconfirm --needed noto-fonts noto-fonts-cjk noto-fonts-emoji \
    ttf-roboto ttf-roboto-mono ttf-roboto-mono-nerd \
    ttf-ubuntu-font-family ttf-ubuntu-mono-nerd ttf-ubuntu-nerd \
    ttf-fira-code otf-firamono-nerd ttf-firacode-nerd \
    ttf-croscore
paru -S --noconfirm --needed noto-fonts-ar

# Spell checkers
sudo pacman -S --noconfirm --needed hunspell nuspell ispell \
    hunspell-en_us
paru -S --noconfirm --needed hunspell-ar

# Apps that i use
sudo pacman -S --noconfirm --needed nemo nemo-fileroller \
    pix xviewer \
    kcalc

# Add user to groups
sudo usermod -a -G wheel,audio,disk,input,kvm,lp,render,storage,uucp,video,gamemode,libvirt,power,flatpak $(whoami)