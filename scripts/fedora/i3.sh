#!/usr/bin/bash

# Xorg
sudo dnf install -y xorg-x11-server-Xorg \
    xorg-x11-drv-amdgpu xorg-x11-drv-ati xorg-x11-drv-evdev xorg-x11-drv-fbdev xorg-x11-drv-intel xorg-x11-drv-libinput xorg-x11-drv-nouveau xorg-x11-drv-openchrome xorg-x11-drv-qxl xorg-x11-drv-vesa xorg-x11-drv-vmware xorg-x11-drv-wacom \
    xorg-x11-xinit xrandr xinput

# Pipewire
sudo dnf install -y pipewire pipewire-plugin-jack pipewire-alsa pipewire-pulseaudio pipewire-utils \
    wireplumber pamixer \
    alsa-utils playerctl \
    pavucontrol helvum

# Window manager and its tools
sudo dnf install -y i3 \
    greetd \
    polkit-gnome xdg-desktop-portal xdg-desktop-portal-gtk \
    kwallet kwallet-pam kwalletmanager \
    numlockx xdotool picom dunst feh flameshot timeshift \
    polybar rofi mpv

# Theme and its tools
sudo dnf install -y lxappearance qt5ct qt6ct kvantum kvantum-qt5 git \
    papirus-icon-theme
git clone https://github.com/EliverLara/Nordic /usr/share/themes/Nordic
git clone https://github.com/vinceliuice/WhiteSur-cursors.git /tmp/WhiteSur-cursors
sudo cp -r /tmp/WhiteSur-cursors/dist /usr/share/icons/WhiteSur-cursors

# Fonts
sudo dnf install -y 'dnf-command(copr)'
sudo dnf copr enable -y aquacash5/nerd-fonts 
sudo dnf install -y google-roboto-fonts google-roboto-mono-fonts \
    google-roboto-slab-fonts google-noto-color-emoji-fonts google-noto-naskh-arabic-ui-fonts google-noto-sans-arabic-fonts google-noto-sans-cjk-fonts google-noto-sans-mono-fonts \
    mozilla-fira-fonts-common mozilla-fira-mono-fonts mozilla-fira-sans-fonts google-arimo-fonts google-cousine-fonts google-tinos-fonts \
    roboto-mono-nerd-fonts ubuntu-mono-nerd-fonts ubuntu-nerd-fonts ubuntu-sans-nerd-fonts fira-code-nerd-fonts fira-mono-nerd-fonts 
# missing, ttf-ubuntu-font-family

# Spell checkers
sudo dnf install -y hunspell nuspell \
    hunspell-en-US hunspell-ar

# Apps that i use
sudo dnf install -y 'dnf-command(copr)'
sudo dnf copr enable -y yselkowitz/xapps
sudo dnf install -y nemo nemo-fileroller \
    kcalc \
    pix xviewer