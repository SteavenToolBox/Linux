#!/usr/bin/bash

# Xorg
sudo apt install -y xserver-xorg xserver-xorg-video-all xserver-xorg-input-libinput

# Pipewire
sudo apt install -y pipewire pipewire-jack pipewire-alsa pipewire-pulse \
    wireplumber pamixer \
    alsa-utils playerctl \
    pavucontrol helvum

# Window manager and its tools
sudo apt install -y i3-wm \
    greetd \
    xdg-desktop-portal xdg-desktop-portal-gtk \
    kwalletcli libpam-kwallet5 libpam-kwallet-common kwalletmanager \
    numlockx xdotool picom dunst feh flameshot timeshift \
    polybar rofi mpv
# missing, polkit-gnome

# Theme and its tools
sudo apt install -y lxappearance qt5ct qt6ct qt5-style-kvantum git \
    papirus-icon-theme
git clone https://github.com/EliverLara/Nordic /usr/share/themes/Nordic
git clone https://github.com/vinceliuice/WhiteSur-cursors.git /tmp/WhiteSur-cursors
sudo cp -r /tmp/WhiteSur-cursors/dist /usr/share/icons/WhiteSur-cursors

# Fonts
sudo apt install -y noto-fonts noto-fonts-cjk noto-fonts-emoji \
    ttf-roboto ttf-roboto-mono ttf-roboto-mono-nerd \
    ttf-ubuntu-font-family ttf-ubuntu-mono-nerd ttf-ubuntu-nerd \
    ttf-fira-code otf-firamono-nerd ttf-firacode-nerd \
    ttf-croscore
paru -S --noconfirm --needed noto-fonts-ar

# Spell checkers
sudo apt install -y hunspell nuspell ispell \
    hunspell-en-us hunspell-ar

# Apps that i use
sudo apt install -y nemo nemo-fileroller \
    kcalc
# missing, pix xviewer

# Add user to groups
sudo usermod -a -G wheel,audio,disk,input,kvm,lp,render,storage,uucp,video,gamemode,libvirt,power,flatpak $(whoami)