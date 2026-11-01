"""Sway Wayland Compositor Installation Module.

Installs and configures the complete Sway environment:
- Wayland display protocol and XWayland compatibility
- Pipewire audio architecture
- Sway window manager, Waybar, Rofi-wayland, Grim/Grimshot, SwayNC
- Nordic theme, WhiteSur cursors, and Nerd fonts
- Nemo file manager
"""

from typing import Optional

from steaventoolbox.core import (
    DistroType,
    add_user_to_groups,
    apt_install,
    aur_install,
    detect_distro,
    dnf_install,
    enable_copr,
    ensure_toolbox_dirs,
    log_header,
    log_success,
    pacman_install,
    run_cmd,
)

SWAY_DEFAULT_GROUPS = [
    "wheel", "audio", "disk", "input", "kvm", "lp", "render",
    "storage", "uucp", "video", "gamemode", "libvirt", "power", "flatpak"
]


def install_sway_arch() -> None:
    """Install Sway setup on Arch Linux."""
    log_header("Installing Sway Window Manager (Arch Linux)")

    pacman_install([
        "wayland", "xorg-xwayland", "qt5-wayland", "qt6-wayland", "wayland-protocols", "lib32-wayland",
        "pipewire", "pipewire-jack", "pipewire-alsa", "pipewire-pulse",
        "lib32-pipewire", "lib32-pipewire-jack", "wireplumber", "pamixer",
        "alsa-utils", "playerctl", "pavucontrol", "helvum",
        "sway", "swayidle", "swaylock-effects", "swaync",
        "greetd", "polkit-gnome", "xdg-desktop-portal", "xdg-desktop-portal-gtk", "xdg-desktop-portal-wlr",
        "kwallet", "kwallet-pam", "kwallet5", "kwalletmanager",
        "grim", "grimshot", "wlsunset", "waybar", "rofi-wayland", "mpv",
        "lxappearance", "qt5ct", "qt6ct", "kvantum", "kvantum-qt5",
        "nordic-theme-git", "papirus-icon-theme", "papirus-folders",
        "noto-fonts", "noto-fonts-cjk", "noto-fonts-emoji",
        "ttf-roboto", "ttf-roboto-mono", "ttf-roboto-mono-nerd",
        "ttf-ubuntu-font-family", "ttf-ubuntu-mono-nerd", "ttf-ubuntu-nerd",
        "ttf-fira-code", "otf-firamono-nerd", "ttf-firacode-nerd", "ttf-croscore",
        "hunspell", "nuspell", "ispell", "hunspell-en_us",
        "nemo", "nemo-fileroller", "pix", "xviewer", "kcalc"
    ])

    aur_install(["whitesur-cursor-theme-git", "noto-fonts-ar", "hunspell-ar"])
    add_user_to_groups(SWAY_DEFAULT_GROUPS)
    log_success("Arch Linux Sway installation complete.")


def install_sway_fedora() -> None:
    """Install Sway setup on Fedora."""
    log_header("Installing Sway Window Manager (Fedora)")

    dnf_install([
        "xorg-x11-server-Xwayland", "qt5-qtwayland", "qt6-qtwayland", "wayland-protocols-devel",
        "pipewire", "pipewire-plugin-jack", "pipewire-alsa", "pipewire-pulseaudio", "pipewire-utils",
        "wireplumber", "pamixer", "alsa-utils", "playerctl", "pavucontrol", "helvum"
    ])

    run_cmd(["dnf", "install", "-y", "dnf-command(copr)"], sudo=True, check=False)
    enable_copr("tofik/sway")
    enable_copr("pheeef/swaylock-effects")

    dnf_install([
        "sway", "swayidle", "swaylock-effects", "swaync", "greetd",
        "polkit-gnome", "xdg-desktop-portal", "xdg-desktop-portal-gtk", "xdg-desktop-portal-wlr",
        "kwallet", "kwallet-pam", "kwalletmanager", "grim", "grimshot", "wlsunset",
        "waybar", "rofi-wayland", "mpv", "lxappearance", "qt5ct", "qt6ct", "kvantum",
        "kvantum-qt5", "git", "papirus-icon-theme"
    ])

    enable_copr("aquacash5/nerd-fonts")
    dnf_install([
        "google-roboto-fonts", "google-roboto-mono-fonts", "google-roboto-slab-fonts",
        "google-noto-color-emoji-fonts", "google-noto-naskh-arabic-ui-fonts",
        "google-noto-sans-arabic-fonts", "google-noto-sans-cjk-fonts", "google-noto-sans-mono-fonts",
        "mozilla-fira-fonts-common", "mozilla-fira-mono-fonts", "mozilla-fira-sans-fonts",
        "google-arimo-fonts", "google-cousine-fonts", "google-tinos-fonts",
        "roboto-mono-nerd-fonts", "ubuntu-mono-nerd-fonts", "ubuntu-nerd-fonts",
        "ubuntu-sans-nerd-fonts", "fira-code-nerd-fonts", "fira-mono-nerd-fonts",
        "hunspell", "nuspell", "hunspell-en-US", "hunspell-ar"
    ])

    enable_copr("yselkowitz/xapps")
    dnf_install(["nemo", "nemo-fileroller", "kcalc", "pix", "xviewer"])

    run_cmd("git clone https://github.com/EliverLara/Nordic /usr/share/themes/Nordic", shell=True, sudo=True, check=False)
    run_cmd("git clone https://github.com/vinceliuice/WhiteSur-cursors.git /tmp/WhiteSur-cursors && sudo cp -r /tmp/WhiteSur-cursors/dist /usr/share/icons/WhiteSur-cursors", shell=True, sudo=True, check=False)

    add_user_to_groups(SWAY_DEFAULT_GROUPS)
    log_success("Fedora Sway installation complete.")


def install_sway_ubuntu() -> None:
    """Install Sway setup on Ubuntu / Debian."""
    log_header("Installing Sway Window Manager (Ubuntu / Debian)")

    apt_install([
        "wayland-protocols", "xwayland", "qt5-qpa-platformtheme-xdgdesktopportal",
        "pipewire", "pipewire-jack", "pipewire-alsa", "pipewire-pulse",
        "wireplumber", "pamixer", "alsa-utils", "playerctl", "pavucontrol", "helvum",
        "sway", "swayidle", "greetd",
        "xdg-desktop-portal", "xdg-desktop-portal-gtk", "xdg-desktop-portal-wlr",
        "kwalletcli", "libpam-kwallet5", "libpam-kwallet-common", "kwalletmanager",
        "grim", "wlsunset", "waybar", "mpv",
        "lxappearance", "qt5ct", "qt6ct", "qt5-style-kvantum", "git", "papirus-icon-theme",
        "fonts-noto", "fonts-noto-cjk", "fonts-noto-color-emoji", "fonts-roboto", "fonts-firacode",
        "hunspell", "nuspell", "ispell", "hunspell-en-us", "hunspell-ar",
        "nemo", "nemo-fileroller", "kcalc"
    ])

    run_cmd("git clone https://github.com/EliverLara/Nordic /usr/share/themes/Nordic", shell=True, sudo=True, check=False)
    run_cmd("git clone https://github.com/vinceliuice/WhiteSur-cursors.git /tmp/WhiteSur-cursors && sudo cp -r /tmp/WhiteSur-cursors/dist /usr/share/icons/WhiteSur-cursors", shell=True, sudo=True, check=False)

    add_user_to_groups(SWAY_DEFAULT_GROUPS)
    log_success("Ubuntu / Debian Sway installation complete.")


def install_sway(distro: Optional[DistroType] = None) -> None:
    """Install Sway for the specified or detected distribution."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()

    if active_distro == DistroType.ARCH:
        install_sway_arch()
    elif active_distro == DistroType.FEDORA:
        install_sway_fedora()
    elif active_distro in (DistroType.UBUNTU, DistroType.DEBIAN):
        install_sway_ubuntu()


if __name__ == "__main__":
    install_sway()

