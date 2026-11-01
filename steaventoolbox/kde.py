"""KDE Plasma Desktop Environment Module.

Installs and configures KDE Plasma desktop environment, SDDM display manager,
Wayland, Pipewire, Kvantum/Breeze styling, fonts, and KDE application suite.
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

KDE_DEFAULT_GROUPS = [
    "wheel", "audio", "disk", "input", "kvm", "lp", "render",
    "storage", "uucp", "video", "gamemode", "libvirt", "power", "flatpak"
]


def install_kde_arch() -> None:
    """Install KDE Plasma Desktop Environment on Arch Linux."""
    log_header("Installing KDE Plasma Desktop (Arch Linux)")

    pacman_install([
        "xorg", "xorg-server", "xorg-apps", "xorg-xinit", "xorg-xwayland",
        "wayland", "qt5-wayland", "qt6-wayland", "wayland-protocols", "lib32-wayland",
        "pipewire", "pipewire-jack", "pipewire-alsa", "pipewire-pulse",
        "lib32-pipewire", "lib32-pipewire-jack", "wireplumber", "pamixer",
        "alsa-utils", "playerctl", "pavucontrol", "helvum",
        "plasma-desktop", "plasma-nm", "plasma-pa", "kscreen",
        "sddm", "sddm-kcm", "flatpak-kcm", "polkit-gnome",
        "xdg-desktop-portal", "xdg-desktop-portal-kde",
        "kwallet", "kwallet-pam", "kwallet5", "kwalletmanager", "spectacle",
        "kvantum", "kvantum-qt5", "kde-gtk-config", "breeze-gtk",
        "nordic-theme-git", "papirus-icon-theme", "papirus-folders",
        "noto-fonts", "noto-fonts-cjk", "noto-fonts-emoji",
        "ttf-roboto", "ttf-roboto-mono", "ttf-roboto-mono-nerd",
        "ttf-ubuntu-font-family", "ttf-ubuntu-mono-nerd", "ttf-ubuntu-nerd",
        "ttf-fira-code", "otf-firamono-nerd", "ttf-firacode-nerd", "ttf-croscore",
        "hunspell", "nuspell", "ispell", "hunspell-en_us",
        "dolphin", "ark", "konsole", "spectacle", "kcalc", "kate", "gwenview"
    ])

    aur_install(["whitesur-cursor-theme-git", "noto-fonts-ar", "hunspell-ar"])
    add_user_to_groups(KDE_DEFAULT_GROUPS)
    log_success("Arch Linux KDE Plasma installation complete.")


def install_kde(distro: Optional[DistroType] = None) -> None:
    """Install KDE Plasma for the specified or detected distribution."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()

    if active_distro == DistroType.ARCH:
        install_kde_arch()
    else:
        log_warning(f"KDE automated setup is configured for Arch Linux (current: {active_distro.value}).")


if __name__ == "__main__":
    install_kde()

