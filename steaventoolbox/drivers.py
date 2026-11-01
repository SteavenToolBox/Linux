"""GPU Detection and Driver Installation Module.

Detects Nvidia, Intel, and AMD GPUs via lspci or sysfs, and installs the
appropriate drivers for Arch Linux, Fedora, Ubuntu, or Debian.
"""

import os
import re
import subprocess
from typing import Dict, Optional

from steaventoolbox.core import (
    DistroType,
    apt_install,
    detect_distro,
    dnf_install,
    ensure_toolbox_dirs,
    log_error,
    log_header,
    log_info,
    log_success,
    log_warning,
    pacman_install,
    run_cmd,
)


def detect_gpus() -> Dict[str, bool]:
    """Detect presence of Nvidia, Intel, or AMD graphics cards.

    Returns:
        Dict[str, bool]: A dictionary mapping 'nvidia', 'intel', 'amd' to a boolean.
    """
    detected = {"nvidia": False, "intel": False, "amd": False}

    try:
        proc = subprocess.run(
            ["lspci"],
            capture_output=True,
            text=True,
            check=False,
        )
        output = proc.stdout
    except FileNotFoundError:
        log_warning("'lspci' command not found. Trying /sys/bus/pci/devices inspection.")
        output = ""

    # Search for VGA or 3D controller lines
    vga_lines = [
        line for line in output.splitlines()
        if re.search(r"VGA compatible controller|3D controller|Display controller", line, re.IGNORECASE)
    ]

    if not vga_lines and not output:
        # Fallback inspection of sysfs
        try:
            import glob
            for uevent in glob.glob("/sys/bus/pci/devices/*/uevent"):
                with open(uevent, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().lower()
                    if "pciclass=03" in content:  # PCI Class 03 is Display controller
                        if "nvidia" in content:
                            detected["nvidia"] = True
                        if "intel" in content:
                            detected["intel"] = True
                        if "amd" in content or "ati" in content:
                            detected["amd"] = True
        except Exception as exc:
            log_warning(f"Failed to scan sysfs: {exc}")

    for line in vga_lines:
        line_lower = line.lower()
        if "nvidia" in line_lower:
            detected["nvidia"] = True
            log_info(f"Found Nvidia hardware: {line.strip()}")
        if "intel" in line_lower:
            detected["intel"] = True
            log_info(f"Found Intel hardware: {line.strip()}")
        if "amd" in line_lower or "ati" in line_lower or "advanced micro devices" in line_lower:
            detected["amd"] = True
            log_info(f"Found AMD hardware: {line.strip()}")

    return detected


def install_gpu_drivers(distro: Optional[DistroType] = None) -> None:
    """Install GPU drivers based on detected hardware and Linux distribution."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()
    log_header("GPU Driver Installer")

    gpus = detect_gpus()
    if not any(gpus.values()):
        log_warning("No dedicated Nvidia, Intel, or AMD GPU detected.")
        return

    if active_distro == DistroType.ARCH:
        _install_arch_gpu_drivers(gpus)
    elif active_distro == DistroType.FEDORA:
        _install_fedora_gpu_drivers(gpus)
    elif active_distro in (DistroType.UBUNTU, DistroType.DEBIAN):
        _install_ubuntu_gpu_drivers(gpus)
    else:
        log_error(f"GPU driver installation is not supported on {active_distro.value}.")


def _install_arch_gpu_drivers(gpus: Dict[str, bool]) -> None:
    """Install Arch Linux GPU packages."""
    if gpus["nvidia"]:
        log_info("Installing Arch Nvidia drivers...")
        cmd = [
            "nvidia-utils", "opencl-nvidia", "nvidia-settings",
            "libva-nvidia-driver", "egl-wayland", "lib32-nvidia-utils", "lib32-opencl-nvidia"
        ]
        kernel = os.uname().release
        if "cachyos" in kernel:
            cmd.insert(0, "linux-cachyos-nvidia-open")
        else:
            cmd.insert(0, "nvidia")
            cmd.insert(1, "nvidia-dkms")
        pacman_install(cmd)

    if gpus["intel"]:
        log_info("Installing Arch Intel drivers...")
        pacman_install([
            "mesa", "vulkan-intel", "intel-media-driver",
            "intel-compute-runtime", "lib32-mesa", "lib32-vulkan-intel"
        ])

    if gpus["amd"]:
        log_info("Installing Arch AMD drivers...")
        pacman_install([
            "mesa", "mesa-vdpau", "vulkan-radeon",
            "libva-mesa-driver", "rocm-opencl-runtime",
            "lib32-mesa", "lib32-mesa-vdpau", "lib32-libva-mesa-driver", "lib32-vulkan-radeon"
        ])

    log_success("Arch GPU drivers installation completed.")


def _install_fedora_gpu_drivers(gpus: Dict[str, bool]) -> None:
    """Install Fedora GPU packages."""
    if gpus["nvidia"]:
        log_info("Installing Fedora Nvidia drivers via RPM Fusion...")
        dnf_install([
            "akmod-nvidia", "xorg-x11-drv-nvidia-cuda",
            "libva-nvidia-driver.i686", "libva-nvidia-driver.x86_64"
        ])

    if gpus["intel"]:
        log_info("Installing Fedora Intel drivers...")
        dnf_install([
            "mesa-vulkan-drivers", "intel-media-driver", "intel-compute-runtime"
        ])

    if gpus["amd"]:
        log_info("Installing Fedora AMD drivers...")
        dnf_install([
            "mesa-vdpau-drivers-freeworld", "mesa-vulkan-drivers",
            "mesa-va-drivers-freeworld", "rocm-opencl"
        ])

    log_success("Fedora GPU drivers installation completed.")


def _install_ubuntu_gpu_drivers(gpus: Dict[str, bool]) -> None:
    """Install Ubuntu / Debian GPU packages."""
    if gpus["nvidia"]:
        log_info("Installing Ubuntu / Debian Nvidia drivers...")
        apt_install(["nvidia-dkms-550-open", "nvidia-driver-550-open"])

    if gpus["intel"]:
        log_info("Installing Ubuntu / Debian Intel drivers...")
        apt_install([
            "libgl1-mesa-dri:i386", "mesa-vulkan-drivers",
            "mesa-vulkan-drivers:i386", "intel-opencl-icd"
        ])

    if gpus["amd"]:
        log_info("Installing Ubuntu / Debian AMD drivers...")
        apt_install([
            "libgl1-mesa-dri:i386", "mesa-vulkan-drivers",
            "mesa-vulkan-drivers:i386", "mesa-va-drivers", "mesa-vdpau-drivers"
        ])

    log_success("Ubuntu / Debian GPU drivers installation completed.")


if __name__ == "__main__":
    install_gpu_drivers()
