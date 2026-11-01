"""Applications and Productivity Suite Module.

Installs CLI utilities, desktop applications, disk management tools,
and background services (SSH & Syncthing) across:
- Arch Linux
- Fedora Linux
- Ubuntu & Debian
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
    get_real_user,
    log_header,
    log_success,
    pacman_install,
    run_cmd,
)

APPS_DEFAULT_GROUPS = [
    "wheel", "audio", "disk", "input", "kvm", "lp", "render",
    "storage", "uucp", "video", "gamemode", "libvirt", "power", "flatpak"
]


def install_apps_arch() -> None:
    """Install standard applications on Arch Linux."""
    log_header("Installing Applications (Arch Linux)")

    # CLI apps
    pacman_install([
        "starship", "zoxide", "fastfetch", "trash-cli", "bat", "speedtest-cli",
        "neovim", "vim", "nano", "unzip", "unrar", "neofetch", "hyfetch",
        "xclip", "lolcat", "eza", "github-cli", "topgrade"
    ])

    # Desktop apps
    pacman_install([
        "bitwarden", "discord", "whatsie-git", "element-desktop",
        "visual-studio-code-bin", "github-desktop", "libreoffice-fresh",
        "xreader", "notepadqq", "phonon-qt6-mpv", "obs-studio-stable",
        "obs-vkcapture", "lib32-obs-vkcapture", "gstreamer-vaapi", "obs-gstreamer",
        "gimp", "kdenlive", "mediainfo", "mediainfo-gui",
        "qbittorrent", "freedownloadmanager", "firefox", "vlc", "audacious"
    ])

    aur_install(["nemo-mediainfo-tab", "ente-auth-bin", "obs-pipewire-audio-capture-bin"])

    # Disks utilities
    pacman_install([
        "gnome-disk-utility", "gparted", "dosfstools", "btrfs-progs",
        "ntfs-3g", "exfatprogs", "mtools"
    ])

    # Ecosystem: SSH & Syncthing
    pacman_install(["openssh", "syncthing", "syncthingtray-qt6"])
    run_cmd(["systemctl", "enable", "--now", "sshd"], sudo=True, check=False)

    user = get_real_user()
    if user and user != "root":
        run_cmd(["systemctl", "enable", "--now", f"syncthing@{user}"], sudo=True, check=False)

    add_user_to_groups(APPS_DEFAULT_GROUPS)
    log_success("Arch Linux applications installation complete.")


def install_apps_fedora() -> None:
    """Install standard applications on Fedora."""
    log_header("Installing Applications (Fedora)")

    run_cmd(["dnf", "install", "-y", "dnf-command(copr)"], sudo=True, check=False)
    enable_copr("atim/starship")
    dnf_install([
        "starship", "zoxide", "fastfetch", "trash-cli", "bat", "speedtest-cli",
        "neovim", "vim", "nano", "unzip", "unrar", "neofetch", "hyfetch",
        "xclip", "lolcat", "eza", "gh", "flatpak"
    ])

    enable_copr("sergiomb/electrons")
    enable_copr("andykimpe/notepadqq")
    dnf_install([
        "discord", "libreoffice", "xreader", "obs-studio", "obs-studio-plugin-vkcapture",
        "gimp", "kdenlive", "mediainfo", "mediainfo-gui", "qbittorrent",
        "firefox", "vlc", "audacious", "element-desktop", "notepadqq"
    ])

    dnf_install([
        "gnome-disk-utility", "gparted", "dosfstools", "btrfs-progs",
        "ntfs-3g", "exfatprogs", "mtools"
    ])

    enable_copr("hazel-bunny/syncthing-unofficial")
    dnf_install(["openssh", "syncthing", "syncthingtray-qt6"])
    run_cmd(["systemctl", "enable", "--now", "sshd"], sudo=True, check=False)

    user = get_real_user()
    if user and user != "root":
        run_cmd(["systemctl", "enable", "--now", f"syncthing@{user}"], sudo=True, check=False)

    add_user_to_groups(APPS_DEFAULT_GROUPS)
    log_success("Fedora applications installation complete.")


def install_apps_ubuntu() -> None:
    """Install standard applications on Ubuntu / Debian."""
    log_header("Installing Applications (Ubuntu / Debian)")

    apt_install([
        "zoxide", "trash-cli", "bat", "speedtest-cli", "neovim", "vim", "nano",
        "unzip", "unrar", "neofetch", "hyfetch", "xclip", "lolcat", "eza", "gh"
    ])

    apt_install([
        "libreoffice", "notepadqq", "obs-studio", "gimp", "kdenlive",
        "mediainfo", "mediainfo-gui", "qbittorrent", "firefox", "vlc", "audacious"
    ])

    apt_install([
        "gnome-disk-utility", "gparted", "dosfstools", "btrfs-progs",
        "ntfs-3g", "exfatprogs", "mtools"
    ])

    apt_install(["openssh-client", "openssh-server", "openssh-sftp-server", "syncthing"])
    run_cmd(["systemctl", "enable", "--now", "sshd"], sudo=True, check=False)

    user = get_real_user()
    if user and user != "root":
        run_cmd(["systemctl", "enable", "--now", f"syncthing@{user}"], sudo=True, check=False)

    add_user_to_groups(APPS_DEFAULT_GROUPS)
    log_success("Ubuntu / Debian applications installation complete.")


def install_apps(distro: Optional[DistroType] = None) -> None:
    """Install application suite for the specified or detected distribution."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()

    if active_distro == DistroType.ARCH:
        install_apps_arch()
    elif active_distro == DistroType.FEDORA:
        install_apps_fedora()
    elif active_distro in (DistroType.UBUNTU, DistroType.DEBIAN):
        install_apps_ubuntu()


if __name__ == "__main__":
    install_apps()

