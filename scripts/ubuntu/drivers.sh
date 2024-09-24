#!/bin/bash

# Function to install Nvidia drivers
install_nvidia() {
    echo "Detected Nvidia GPU(s). Installing Nvidia drivers..."
    sudo apt install -y nvidia-dkms-550-open nvidia-driver-550-open
}

# Function to install Intel drivers
install_intel() {
    echo "Detected Intel GPU(s). Installing Intel drivers..."
    sudo apt install -y libgl1-mesa-dri:i386 mesa-vulkan-drivers mesa-vulkan-drivers:i386 intel-opencl-icd

}

# Function to install AMD drivers
install_amd() {
    echo "Detected AMD GPU(s). Installing AMD drivers..."
    sudo apt install -y libgl1-mesa-dri:i386 mesa-vulkan-drivers mesa-vulkan-drivers:i386 mesa-va-drivers mesa-vdpau-drivers
    # missing, rocm-opencl-runtime

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