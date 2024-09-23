#!/usr/bin/bash

# Proton and Wine
sudo pacman -S --noconfirm --needed proton-ge-custom wine-staging wine-mono wine-gecko

# Tools required for Gaming
sudo pacman -S --noconfirm --needed  mangohud lib32-mangohud gamemode lib32-gamemode gamescope vulkan-tools protontricks winetricks protonplus 

# Lunchers
sudo pacman -S --noconfirm --needed steam lutris heroic-games-launcher-bin 

# Emualtors
sudo pacman -S --noconfirm --needed duckstation rpcs3-git ryujinx dolphin-emu pcsx2-git
paru -S --noconfirm --needed cemu-bin

# Minecraft
sudo pacman -S --noconfirm --needed minecraft-launcher prismlauncher lunar-client jre-openjdk jre21-openjdk jre17-openjdk jre8-openjdk 

# Add user to groups
sudo usermod -a -G wheel,audio,disk,input,storage,video,gamemode,power $(whoami)