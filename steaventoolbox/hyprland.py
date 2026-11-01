"""Hyprland Dynamic Tiling Wayland Compositor Module.

Installs and configures Hyprland, Hypridle, Hyprlock, Waybar, SwayNC,
Rofi-wayland, portal integrations, themes, and terminal tools.
"""

from typing import Optional

from steaventoolbox.core import (
    DistroType,
    add_user_to_groups,
    aur_install,
    detect_distro,
    dnf_install,
    enable_copr,
    ensure_toolbox_dirs,
    log_header,
    log_success,
    log_warning,
    pacman_install,
    run_cmd,
)

HYPRLAND_DEFAULT_GROUPS = [
    "wheel", "audio", "disk", "input", "kvm", "lp", "render",
    "storage", "uucp", "video", "gamemode", "libvirt", "power", "flatpak"
]


def install_hyprland_arch() -> None:
    """Install Hyprland setup on Arch Linux."""
    log_header("Installing Hyprland (Arch Linux)")

    pacman_install([
        "hyprland", "hypridle", "hyprlock", "xdg-desktop-portal",
        "xdg-desktop-portal-hyprland", "xdg-desktop-portal-gtk",
        "swaync", "swaybg", "waybar", "rofi-wayland",
        "kvantum", "kvantum-qt5", "qt5ct", "qt6ct",
        "network-manager-applet", "polkit", "polkit-gnome",
        "kwallet", "kwallet-pam", "kitty"
    ])

    aur_install(["whitesur-cursor-theme-git"])
    add_user_to_groups(HYPRLAND_DEFAULT_GROUPS)
    log_success("Arch Linux Hyprland installation complete.")


def install_hyprland_fedora() -> None:
    """Install Hyprland setup on Fedora."""
    log_header("Installing Hyprland (Fedora)")

    run_cmd(["dnf", "install", "-y", "dnf-command(copr)"], sudo=True, check=False)
    enable_copr("solopasha/hyprland")

    dnf_install([
        "hyprland", "hypridle", "hyprlock", "hyprpicker",
        "xdg-desktop-portal", "xdg-desktop-portal-hyprland", "xdg-desktop-portal-gtk",
        "swaylock-effects", "swaync", "swaybg", "waybar", "rofi-wayland",
        "kvantum", "kvantum-qt5", "qt5ct"
    ])

    add_user_to_groups(HYPRLAND_DEFAULT_GROUPS)
    log_success("Fedora Hyprland installation complete.")


def install_hyprland(distro: Optional[DistroType] = None) -> None:
    """Install Hyprland for the specified or detected distribution."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()

    if active_distro == DistroType.ARCH:
        install_hyprland_arch()
    elif active_distro == DistroType.FEDORA:
        install_hyprland_fedora()
    else:
        log_warning(f"Hyprland automated installer is configured for Arch and Fedora (current: {active_distro.value}).")


if __name__ == "__main__":
    install_hyprland()

