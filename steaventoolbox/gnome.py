"""GNOME Desktop Environment Module.

Installs and configures the GNOME Shell desktop environment, Wayland, Pipewire,
Adwaita and Nordic styling, fonts, and core GNOME utilities.
"""

from typing import Optional

from steaventoolbox.core import (
    DistroType,
    add_user_to_groups,
    aur_install,
    detect_distro,
    ensure_toolbox_dirs,
    log_header,
    log_success,
    log_warning,
    pacman_install,
)

GNOME_DEFAULT_GROUPS = [
    "wheel", "audio", "disk", "input", "kvm", "lp", "render",
    "storage", "uucp", "video", "gamemode", "libvirt", "power", "flatpak"
]


def install_gnome_arch() -> None:
    """Install GNOME Desktop Environment on Arch Linux."""
    log_header("Installing GNOME Desktop (Arch Linux)")

    pacman_install([
        "xorg", "xorg-server", "xorg-apps", "xorg-xinit", "xorg-xwayland",
        "wayland", "qt5-wayland", "qt6-wayland", "wayland-protocols", "lib32-wayland",
        "pipewire", "pipewire-jack", "pipewire-alsa", "pipewire-pulse",
        "lib32-pipewire", "lib32-pipewire-jack", "wireplumber", "pamixer",
        "alsa-utils", "playerctl", "pavucontrol", "helvum",
        "gnome-session", "gnome-shell", "gnome-control-center",
        "gnome-tweaks", "extension-manager", "polkit-gnome",
        "xdg-desktop-portal", "xdg-desktop-portal-gnome", "gnome-keyring",
        "qt5ct", "qt6ct", "kvantum", "kvantum-qt5",
        "adwaita-cursors", "adwaita-icon-theme", "adwaita-icon-theme-legacy",
        "adwaita-qt6", "adwaita-qt5", "kvantum-theme-libadwaita-git",
        "nordic-theme-git", "papirus-icon-theme", "papirus-folders",
        "noto-fonts", "noto-fonts-cjk", "noto-fonts-emoji",
        "ttf-roboto", "ttf-roboto-mono", "ttf-roboto-mono-nerd",
        "ttf-ubuntu-font-family", "ttf-ubuntu-mono-nerd", "ttf-ubuntu-nerd",
        "ttf-fira-code", "otf-firamono-nerd", "ttf-firacode-nerd", "ttf-croscore",
        "hunspell", "nuspell", "ispell", "hunspell-en_us",
        "nautilus", "file-roller", "gnome-terminal", "gnome-screenshot",
        "gnome-text-editor", "eog", "gnome-calculator"
    ])

    aur_install(["whitesur-cursor-theme-git", "noto-fonts-ar", "hunspell-ar"])
    add_user_to_groups(GNOME_DEFAULT_GROUPS)
    log_success("Arch Linux GNOME installation complete.")


def install_gnome(distro: Optional[DistroType] = None) -> None:
    """Install GNOME Desktop Environment for the specified or detected distribution."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()

    if active_distro == DistroType.ARCH:
        install_gnome_arch()
    else:
        log_warning(f"GNOME automated setup is configured for Arch Linux (current: {active_distro.value}).")


if __name__ == "__main__":
    install_gnome()

