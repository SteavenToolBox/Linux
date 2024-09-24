#!/usr/bin/bash

# Wine
sudo apt install -y wine

# Tools required for Gaming
sudo apt install -y  mangohud gamemode vulkan-tools protontricks winetricks protonplus 
# missing, gamescope

# Lunchers
sudo apt install -y steam lutris
# missing, heroic-games-launcher-bin

# Emualtors
sudo apt install -y dolphin-emu 
# missing, duckstation rpcs3 ryujinx pcsx2 cemu


# Minecraft
sudo apt install -y default-jre openjdk-21-jre openjdk-17-jre openjdk-8-jre 
# missing, minecraft-launcher prismlauncher lunar-client

# Add user to groups
sudo usermod -a -G wheel,audio,disk,input,storage,video,gamemode,power $(whoami)