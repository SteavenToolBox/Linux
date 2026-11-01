"""i3 Window Manager Installation Module.

Installs and configures the complete i3 environment:
- Xorg display server
- Pipewire audio architecture
- i3-wm, polybar, rofi, picom compositor, and notification daemons
- Nordic theme, WhiteSur cursors, Papirus icons, and Nerd fonts
- Nemo file manager and terminal tools
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

I3_DEFAULT_GROUPS = [
    "wheel", "audio", "disk", "input", "kvm", "lp", "render",
    "storage", "uucp", "video", "gamemode", "libvirt", "power", "flatpak"
]


def install_i3_arch() -> None:
    """Install i3 setup on Arch Linux."""
    log_header("Installing i3 Window Manager (Arch Linux)")

    pacman_install([
        "xorg", "xorg-server", "xorg-apps", "xorg-xinit", "xorg-xwayland",
        "pipewire", "pipewire-jack", "pipewire-alsa", "pipewire-pulse",
        "lib32-pipewire", "lib32-pipewire-jack", "wireplumber", "pamixer",
        "alsa-utils", "playerctl", "pavucontrol", "helvum",
        "i3-wm", "greetd", "polkit-gnome", "xdg-desktop-portal", "xdg-desktop-portal-gtk",
        "kwallet", "kwallet-pam", "kwallet5", "kwalletmanager",
        "numlockx", "xdotool", "picom", "dunst", "feh", "flameshot", "timeshift",
        "polybar", "rofi", "mpv",
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
    add_user_to_groups(I3_DEFAULT_GROUPS)
    log_success("Arch Linux i3 installation complete.")


def install_i3_fedora() -> None:
    """Install i3 setup on Fedora."""
    log_header("Installing i3 Window Manager (Fedora)")

    dnf_install([
        "xorg-x11-server-Xorg", "xorg-x11-drv-amdgpu", "xorg-x11-drv-ati",
        "xorg-x11-drv-evdev", "xorg-x11-drv-fbdev", "xorg-x11-drv-intel",
        "xorg-x11-drv-libinput", "xorg-x11-drv-nouveau", "xorg-x11-drv-openchrome",
        "xorg-x11-drv-qxl", "xorg-x11-drv-vesa", "xorg-x11-drv-vmware",
        "xorg-x11-drv-wacom", "xorg-x11-xinit", "xrandr", "xinput",
        "pipewire", "pipewire-plugin-jack", "pipewire-alsa",
        "pipewire-pulseaudio", "pipewire-utils", "wireplumber",
        "pamixer", "alsa-utils", "playerctl", "pavucontrol", "helvum",
        "i3", "greetd", "polkit-gnome", "xdg-desktop-portal", "xdg-desktop-portal-gtk",
        "kwallet", "kwallet-pam", "kwalletmanager", "numlockx", "xdotool",
        "picom", "dunst", "feh", "flameshot", "timeshift", "polybar", "rofi", "mpv",
        "lxappearance", "qt5ct", "qt6ct", "kvantum", "kvantum-qt5", "git", "papirus-icon-theme"
    ])

    run_cmd(["dnf", "install", "-y", "dnf-command(copr)"], sudo=True, check=False)
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

    add_user_to_groups(I3_DEFAULT_GROUPS)
    log_success("Fedora i3 installation complete.")


def install_i3_ubuntu() -> None:
    """Install i3 setup on Ubuntu / Debian."""
    log_header("Installing i3 Window Manager (Ubuntu / Debian)")

    apt_install([
        "xserver-xorg", "xserver-xorg-video-all", "xserver-xorg-input-libinput",
        "pipewire", "pipewire-jack", "pipewire-alsa", "pipewire-pulse",
        "wireplumber", "pamixer", "alsa-utils", "playerctl", "pavucontrol", "helvum",
        "i3-wm", "greetd", "xdg-desktop-portal", "xdg-desktop-portal-gtk",
        "kwalletcli", "libpam-kwallet5", "libpam-kwallet-common", "kwalletmanager",
        "numlockx", "xdotool", "picom", "dunst", "feh", "flameshot", "timeshift",
        "polybar", "rofi", "mpv",
        "lxappearance", "qt5ct", "qt6ct", "qt5-style-kvantum", "git", "papirus-icon-theme",
        "fonts-noto", "fonts-noto-cjk", "fonts-noto-color-emoji",
        "fonts-roboto", "fonts-firacode", "fonts-croscore",
        "hunspell", "nuspell", "ispell", "hunspell-en-us", "hunspell-ar",
        "nemo", "nemo-fileroller", "kcalc"
    ])

    run_cmd("git clone https://github.com/EliverLara/Nordic /usr/share/themes/Nordic", shell=True, sudo=True, check=False)
    run_cmd("git clone https://github.com/vinceliuice/WhiteSur-cursors.git /tmp/WhiteSur-cursors && sudo cp -r /tmp/WhiteSur-cursors/dist /usr/share/icons/WhiteSur-cursors", shell=True, sudo=True, check=False)

    add_user_to_groups(I3_DEFAULT_GROUPS)
    log_success("Ubuntu / Debian i3 installation complete.")


def install_i3(distro: Optional[DistroType] = None) -> None:
    """Install i3 Window Manager for the specified or detected distribution."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()

    if active_distro == DistroType.ARCH:
        install_i3_arch()
    elif active_distro == DistroType.FEDORA:
        install_i3_fedora()
    elif active_distro in (DistroType.UBUNTU, DistroType.DEBIAN):
        install_i3_ubuntu()


if __name__ == "__main__":
    install_i3()

