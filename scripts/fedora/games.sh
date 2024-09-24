#!/usr/bin/bash

# Wine
sudo dnf install -y wine wine-mono

# Tools required for Gaming
sudo dnf install -y 'dnf-command(copr)'
sudo dnf copr enable -y wehagy/protonplus 
sudo dnf install -y mangohud gamemode gamescope vulkan-tools protontricks winetricks protonplus 

# Lunchers
sudo dnf copr enable -y atim/heroic-games-launcher 
sudo dnf install -y steam lutris heroic-games-launcher-bin 

# Emualtors
sudo dnf install -y dolphin-emu 
# missing, duckstation rpcs3 ryujinx pcsx2 cemu

# Minecraft
sudo dnf copr enable -y g3tchoo/prismlauncher
sudo dnf install -y prismlauncher java-latest-openjdk java-21-openjdk java-17-openjdk java-1.8.0-openjdk 
# missing, minecraft-launcher lunar-client

# Add user to groups
sudo usermod -a -G wheel,audio,disk,input,storage,video,gamemode,power $(whoami)