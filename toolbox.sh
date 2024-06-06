#!/bin/bash
RUN=1 # run flag
# Check for required tools at the start
if command -v wget &> /dev/null; then
    echo "wget is already installed."
else
    echo "wget could not be found, installing it."
    sudo pacman -S --noconfirm --needed wget
fi

if command -v yay &> /dev/null; then
    echo "yay is already installed."
else
    echo "yay could not be found, installing it."
    sudo pacman -Syu --noconfirm --needed git base-devel
    git clone https://aur.archlinux.org/yay-bin.git && cd yay-bin/ && makepkg -si --noconfirm
fi

while [ $RUN = 1 ] # while run flag equals 1 - reopening menu after each action
do
  echo ================================================================
  echo "SteavenToolbox-For-Arch | We care about your pc!" "Arch Linux!"
  echo ================================================================
  echo "1. Update Arch Linux"
  echo "2. Install Core Linux Packages required for any desktop environment / window manager"
  echo "3. Install Gnome"
  echo "4. Install Kde"
  echo "5. Install i3"
  echo "6. Install Hyprland"
  echo "0. Exit"
  read -p "Type the number." ANSWER

  if [ $ANSWER == "0" ]; then
    exit
  fi

  if [ $ANSWER == "1" ]; then
    clear
    echo "Updating Arch Linux Pacman Packages"
    sudo pacman -Syu --noconfirm --needed
    echo "Updating Arch Snaps"
    sudo snap refresh
    echo "Updating Arch Flatpaks"
    sudo flatpak update -y
  fi
  if [ $ANSWER == "2" ]; then
    clear
    wget -O core-packages.txt https://raw.githubusercontent.com/SteavenToolBox/Arch/main/core-packages.txt
    yay -Syu --noconfirm --needed $(cat core-packages.txt)
  fi

  if [ $ANSWER == "3" ]; then
    wget -O gnome-packages.txt https://raw.githubusercontent.com/SteavenToolBox/Arch/main/gnome-packages.txt
    yay -Syu --noconfirm --needed $(cat gnome-packages.txt)
  fi
  if [ $ANSWER == "4" ]; then
    wget -O kde-packages.txt https://raw.githubusercontent.com/SteavenToolBox/Arch/main/kde-packages.txt
    yay -Syu --noconfirm --needed $(cat kde-packages.txt)
  fi
  if [ $ANSWER == "5" ]; then
    wget -O i3-packages.txt https://raw.githubusercontent.com/SteavenToolBox/Arch/main/i3-packages.txt
    yay -Syu --noconfirm --needed $(cat i3-packages.txt)
  fi
  if [ $ANSWER == "6" ]; then
    wget -O hyprland-packages.txt https://raw.githubusercontent.com/SteavenToolBox/Arch/main/hyprland-packages.txt
    yay -Syu --noconfirm --needed $(cat hyprland-packages.txt)
  else
    echo "Quitting..."
    RUN=1 # set run flag to 0 so program will end
  fi
done