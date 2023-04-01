#!/bin/bash
RUN=1 # run flag
while [ $RUN = 1 ] # while run flag equals 1 - reopening menu after each action
do
  clear
  echo ================================================================
  echo "SteavenToolbox-For-Arch | We care about your pc!" "Arch Linux!"
  echo ================================================================
  echo "1. Update Arch Linux"
  echo "2. Install Needed Arch Linux Apps Apps"
  echo "3. Replace Snap Store with Gnome Software"
  echo "4. Install ZSH with Power10k and zsh autocompilte"
  echo "5. Install i3"
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
  echo "Installing VLC and MPV"
  sudo pacman -S --noconfirm --needed vlv mp
  fi

  if [ $ANSWER == "3" ]; then
  echo "Removing Snap store"
  sudo snap remove snap-store
  echo "Installing and Configuring Flatpak"
  sudo pacman -S --noconfirm --needed flatpak 
  sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
  echo "Installing Gnome Software"
  sudo pacman -S --noconfirm --needed gnome-software 
  fi
  if [ $ANSWER == "4" ]; then
  echo "Installing Fonts"
  wget https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/FiraCode.zip
  wget https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Meslo.zip
  sudo unzip FiraCode.zip -d "/usr/share/fonts"
  sudo unzip Meslo.zip -d "/usr/share/fonts"
  sudo fc-cache -vf
  rm ./FiraCode.zip ./Meslo.zip
  echo "Installing ZSH"
  sudo pacman -S --noconfirm --needed zsh zsh-syntax-highlighting autojump zsh-autosuggestions git
  echo "Installing Powerlevel10k"
  mkdir ~/.zsh
  mkdir ~/.zsh/plugins/
  git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/.zsh/plugins/powerlevel10k
  echo 'source ~/.zsh/plugins/powerlevel10k/powerlevel10k.zsh-theme' >> ~/.zshrc
  echo "Installing ZSH AutoComplete"
  git clone --depth 1 -- https://github.com/marlonrichert/zsh-autocomplete.git ~/.zsh/plugins/zsh-autocomplete
  echo 'source ~/.zsh/plugins/zsh-autocomplete/zsh-autocomplete.plugin.zsh' >> ~/.zshrc
  echo 'skip_global_compinit=1' >> ~/.zshenv
  echo "Making zsh Default Shell"
  chsh -s $(which zsh)
  fi
  if [ $ANSWER == "5" ]; then
  sudo apt update
  sudo apt install i3 -y
  else
    echo "Quitting..."
    RUN=1 # set run flag to 0 so program will end
  fi
done