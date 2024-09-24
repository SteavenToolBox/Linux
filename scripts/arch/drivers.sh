#!/bin/bash

# Function to install Nvidia drivers
install_nvidia() {
    echo "Detected Nvidia GPU(s). Installing Nvidia drivers..."
    sudo pacman -S --noconfirm --needed linux-cachyos-nvidia-open nvidia-utils opencl-nvidia nvidia-settings libva-nvidia-driver egl-wayland lib32-nvidia-utils lib32-opencl-nvidia
}

# Function to install Intel drivers
install_intel() {
    echo "Detected Intel GPU(s). Installing Intel drivers..."
    sudo pacman -S --noconfirm --needed mesa vulkan-intel intel-media-driver intel-compute-runtime lib32-mesa lib32-vulkan-intel
}

# Function to install AMD drivers
install_amd() {
    echo "Detected AMD GPU(s). Installing AMD drivers..."
    sudo pacman -S --noconfirm --needed mesa mesa-vdpau vulkan-radeon libva-mesa-driver rocm-opencl-runtime lib32-mesa lib32-mesa-vdpau lib32-libva-mesa-driver lib32-vulkan-radeon
}

# Detect GPUs
gpu_info=$(lspci | grep -E "VGA|3D")

nvidia_found=false
intel_found=false
amd_found=false

while read -r line; do
    if echo "$line" | grep -qi "nvidia"; then
        nvidia_found=true
    elif echo "$line" | grep -qi "intel"; then
        intel_found=true
    elif echo "$line" | grep -qi "amd"; then
        amd_found=true
    fi
done <<< "$gpu_info"

# Install drivers based on detected GPUs
if $nvidia_found; then
    install_nvidia
fi

if $intel_found; then
    install_intel
fi

if $amd_found; then
    install_amd
fi

if ! $nvidia_found && ! $intel_found && ! $amd_found; then
    echo "No supported GPU detected."
fi