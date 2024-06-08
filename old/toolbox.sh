#!/bin/bash
RUN=1 # run flag
# Check for required tools at the start
if command -v wget &> /dev/null; then
    echo "wget is already installed."
else
    echo "wget could not be found, installing it."
    sudo pacman -Syu --noconfirm --needed wget
fi

if command -v yay &> /dev/null; then
    echo "yay is already installed."
else
    echo "yay could not be found, installing it."
    sudo pacman -Syu --noconfirm --needed git base-devel
    git clone https://aur.archlinux.org/yay-bin.git && cd yay-bin/ && makepkg -si --noconfirm
fi

if command -v topgrade &> /dev/null; then
    echo "topgrade is already installed."
else
    echo "topgrade could not be found, installing it."
    yay -Syu --noconfirm --needed topgrade
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
  echo "7. Install Nvidia Beta Drivers for explict sync"
  echo "8. Install SteavenSettings Incloudes Settings that fixs nvidia beta drivers as well"
  echo "9. Install SteavenGamerYT Dot Files, backup your old dot files, this will delete your current ones"
  echo "0. Exit"
  read -p "Type the number." ANSWER

  if [ $ANSWER == "0" ]; then
    exit
  fi

  if [ $ANSWER == "1" ]; then
    clear
    topgrade
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
  fi
  if [ $ANSWER == "7" ]; then
    yay -Syu --noconfirm --needed aur/lib32-nvidia-utils-beta aur/lib32-opencl-nvidia-beta aur/nvidia-beta-dkms aur/nvidia-settings-beta aur/nvidia-utils-beta aur/opencl-nvidia-beta
    sudo systemctl enable nvidia-suspend.service
    sudo systemctl enable nvidia-resume.service
    sudo systemctl enable nvidia-hibernate.service
  fi
  if [ $ANSWER == "8" ]; then
    git clone https://github.com/SteavenGamerYT/SteavenSettings
    cd SteavenSettings
    ./install.sh
  fi
  if [ $ANSWER == "9" ]; then
    cd ~
    yay -Syu --noconfirm --needed starship zsh zsh-syntax-highlighting autojump zsh-autosuggestions zsh-completions neofetch xclip lolcat git trash-cli bat
    mkdir -p ~/Documents/GitHub ~/.zsh/plugins/ ~/.ssh ~/.config
    git clone https://github.com/SteavenGamerYT/dot-files ~/Documents/GitHub/dot-files
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/.zsh/plugins/powerlevel10k
    git clone --depth=1 https://github.com/marlonrichert/zsh-autocomplete.git ~/.zsh/plugins/zsh-autocomplete
    rm -rf ~/.steavengameryt ~/.bash-default ~/.zshrc ~/.bashrc ~/.profile ~/.zshenv ~/.p10k.zsh ~/.config/i3 ~/.config/picom ~/.config/neofetch ~/.config/polybar ~/.config/kitty ~/.config/BetterDiscord ~/.config/hypr ~/.config/waybar ~/.config/starship.toml ~/.config/ulauncher ~/.config/yay ~/.config/MangoHud ~/.ssh/config ~/.config/fish ~/.config/dunst ~/.config/swaylock ~/.config/rofi ~/.config/starship /.config/swaync ~/.zprofile ~/.config/fastfetch ~/.config/betterlockscreen
    ln -s ~/Documents/GitHub/dot-files/.steavengameryt ~/.steavengameryt
    ln -s ~/Documents/GitHub/dot-files/.bash-default ~/.bash-default
    ln -s ~/Documents/GitHub/dot-files/.zshrc ~/.zshrc
    ln -s ~/Documents/GitHub/dot-files/.bashrc ~/.bashrc
    ln -s ~/Documents/GitHub/dot-files/.profile ~/.profile
    ln -s ~/Documents/GitHub/dot-files/.zprofile ~/.zprofile
    ln -s ~/Documents/GitHub/dot-files/.zshenv ~/.zshenv
    ln -s ~/Documents/GitHub/dot-files/.p10k.zsh ~/.p10k.zsh
    ln -s ~/Documents/GitHub/dot-files/.config/i3 ~/.config/i3
    ln -s ~/Documents/GitHub/dot-files/.config/picom ~/.config/picom
    ln -s ~/Documents/GitHub/dot-files/.config/neofetch/ ~/.config/neofetch
    ln -s ~/Documents/GitHub/dot-files/.config/polybar ~/.config/polybar
    ln -s ~/Documents/GitHub/dot-files/.config/kitty ~/.config/kitty
    ln -s ~/Documents/GitHub/dot-files/.config/BetterDiscord ~/.config/BetterDiscord
    ln -s ~/Documents/GitHub/dot-files/.config/hypr ~/.config/hypr
    ln -s ~/Documents/GitHub/dot-files/.config/waybar ~/.config/waybar
    ln -s ~/Documents/GitHub/dot-files/.config/starship ~/.config/starship
    ln -s ~/Documents/GitHub/dot-files/.config/ulauncher ~/.config/ulauncher
    ln -s ~/Documents/GitHub/dot-files/.config/yay ~/.config/yay
    ln -s ~/Documents/GitHub/dot-files/.config/MangoHud ~/.config/MangoHud
    ln -s ~/Documents/GitHub/dot-files/.ssh/config ~/.ssh/config
    ln -s ~/Documents/GitHub/dot-files/.config/fish ~/.config/fish
    ln -s ~/Documents/GitHub/dot-files/.config/dunst ~/.config/dunst
    ln -s ~/Documents/GitHub/dot-files/.config/swaylock ~/.config/swaylock
    ln -s ~/Documents/GitHub/dot-files/.config/rofi ~/.config/rofi
    ln -s ~/Documents/GitHub/dot-files/.config/swaync ~/.config/swaync
    ln -s ~/Documents/GitHub/dot-files/.config/fastfetch ~/.config/fastfetch
    ln -s ~/Documents/GitHub/dot-files/.config/betterlockscreen ~/.config/betterlockscreen
    chsh -s $(which zsh)
  else
    echo "Quitting..."
    RUN=1 # set run flag to 0 so program will end
  fi
done