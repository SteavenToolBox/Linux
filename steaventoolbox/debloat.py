"""System Debloat Module.

Removes pre-installed bloatware, telemetry, and unnecessary default packages
from Fedora and Ubuntu systems.
"""

from typing import List, Optional

from steaventoolbox.core import (
    DistroType,
    detect_distro,
    ensure_toolbox_dirs,
    log_header,
    log_info,
    log_success,
    log_warning,
    run_cmd,
)

# Canonical list of packages to debloat on Fedora
FEDORA_DEBLOAT_PACKAGES: List[str] = [
    "abrt*", "adcli", "alsa-sof-firmware", "anaconda*", "anthy-unicode",
    "atmel-firmware", "bluez-cups", "boost-date-time", "brasero-libs",
    "cheese", "cyrus-sasl-plain", "dos2unix", "eog", "evince", "evince-djvu",
    "fedora-bookmarks", "fedora-chromium-config", "firefox", "geolite2*",
    "gnome-backgrounds", "gnome-boxes", "gnome-calculator", "gnome-calendar",
    "gnome-characters", "gnome-classic-session", "gnome-clocks",
    "gnome-color-manager", "gnome-connections", "gnome-contacts",
    "gnome-font-viewer", "gnome-logs", "gnome-maps", "gnome-remote-desktop",
    "gnome-shell-extension*", "gnome-shell-extension-background-logo",
    "gnome-text-editor", "gnome-themes-extra", "gnome-tour", "gnome-user-docs",
    "gnome-weather", "hyperv*", "kpartx", "libertas-usb8388-firmware", "loupe",
    "mailcap", "mediawriter", "ModemManager", "mozilla-filesystem", "mtr",
    "nano-default-editor", "NetworkManager-ssh", "nmap-ncat", "openconnect",
    "open-vm-tools", "openvpn", "orca", "ppp", "pptp", "qemu-guest-agent",
    "qgnomeplatform", "realmd", "rsync", "samba-client", "simple-scan",
    "snapshot", "sos", "spice-vdagent", "sssd", "tcpdump", "teamd",
    "thermald", "totem", "traceroute", "trousers", "virtualbox-guest-additions",
    "vpnc", "xorg-x11-drv-vmware", "yelp", "zd1211-firmware"
]

# Canonical list of packages to debloat on Ubuntu
UBUNTU_DEBLOAT_PACKAGES: List[str] = [
    "aisleriot", "eog", "evince*", "gnome-calculator",
    "gnome-calendar", "gnome-characters", "gnome-font-viewer", "gnome-logs",
    "gnome-mahjongg", "gnome-remote-desktop", "gnome-shell-extension-manager",
    "gnome-shell-extensions", "gnome-sudoku", "gnome-text-editor",
    "gnome-user-docs", "libreoffice*", "network-manager-openvpn",
    "network-manager-openvpn-gnome", "openvpn", "remmina*", "rhythmbox*",
    "shotwell*", "simple-scan", "transmission*", "ubuntu-docs", "ubuntu-report",
    "vim*"
]


def debloat_fedora() -> None:
    """Purge bloatware packages on Fedora using dnf."""
    log_header("Debloating Fedora Linux")
    log_info(f"Removing {len(FEDORA_DEBLOAT_PACKAGES)} unwanted packages...")
    run_cmd(["dnf", "remove", "-y"] + FEDORA_DEBLOAT_PACKAGES, sudo=True, check=False)
    log_success("Fedora debloat completed.")


def debloat_ubuntu() -> None:
    """Purge bloatware packages on Ubuntu using apt."""
    log_header("Debloating Ubuntu Linux")
    log_info(f"Purging {len(UBUNTU_DEBLOAT_PACKAGES)} unwanted packages...")
    run_cmd(["apt", "purge", "-y"] + UBUNTU_DEBLOAT_PACKAGES, sudo=True, check=False)
    log_success("Ubuntu debloat completed.")


def debloat_system(distro: Optional[DistroType] = None) -> None:
    """Debloat the specified or detected distribution."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()

    if active_distro == DistroType.FEDORA:
        debloat_fedora()
    elif active_distro == DistroType.UBUNTU:
        debloat_ubuntu()
    elif active_distro == DistroType.ARCH:
        log_warning("Arch Linux is already minimal; debloating is not required.")
    elif active_distro == DistroType.DEBIAN:
        log_warning("Debian does not have an automated debloat profile configured.")
    else:
        log_warning(f"Debloating is not supported for {active_distro.value}.")


if __name__ == "__main__":
    debloat_system()

