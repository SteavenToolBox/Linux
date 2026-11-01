"""Gaming Software Suite Module.

Installs gaming tools, compatibility layers, launchers, and emulators across:
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
    log_header,
    log_success,
    pacman_install,
    run_cmd,
)

GAMING_USER_GROUPS = [
    "wheel", "audio", "disk", "input", "storage", "video", "gamemode", "power"
]


def install_games_arch() -> None:
    """Install gaming suite on Arch Linux."""
    log_header("Installing Gaming Suite (Arch Linux)")

    # Wine and Proton
    pacman_install(["proton-ge-custom", "wine-staging", "wine-mono", "wine-gecko"])

    # Gaming utilities
    pacman_install([
        "mangohud", "lib32-mangohud", "gamemode", "lib32-gamemode",
        "gamescope", "vulkan-tools", "protontricks", "winetricks", "protonplus"
    ])

    # Launchers
    pacman_install(["steam", "lutris", "heroic-games-launcher-bin"])

    # Emulators
    pacman_install(["duckstation", "rpcs3-git", "ryujinx", "dolphin-emu", "pcsx2-git"])
    aur_install(["cemu-bin"])

    # Minecraft and Java runtimes
    pacman_install([
        "minecraft-launcher", "prismlauncher", "lunar-client",
        "jre-openjdk", "jre21-openjdk", "jre17-openjdk", "jre8-openjdk"
    ])

    add_user_to_groups(GAMING_USER_GROUPS)
    log_success("Arch Linux gaming suite installation complete.")


def install_games_fedora() -> None:
    """Install gaming suite on Fedora."""
    log_header("Installing Gaming Suite (Fedora)")

    dnf_install(["wine", "wine-mono"])

    run_cmd(["dnf", "install", "-y", "dnf-command(copr)"], sudo=True, check=False)
    enable_copr("wehagy/protonplus")
    dnf_install([
        "mangohud", "gamemode", "gamescope", "vulkan-tools",
        "protontricks", "winetricks", "protonplus"
    ])

    enable_copr("atim/heroic-games-launcher")
    dnf_install(["steam", "lutris", "heroic-games-launcher-bin"])
    dnf_install(["dolphin-emu"])

    enable_copr("g3tchoo/prismlauncher")
    dnf_install([
        "prismlauncher", "java-latest-openjdk", "java-21-openjdk",
        "java-17-openjdk", "java-1.8.0-openjdk"
    ])

    add_user_to_groups(GAMING_USER_GROUPS)
    log_success("Fedora gaming suite installation complete.")


def install_games_ubuntu() -> None:
    """Install gaming suite on Ubuntu / Debian."""
    log_header("Installing Gaming Suite (Ubuntu / Debian)")

    apt_install(["wine"])
    apt_install(["mangohud", "gamemode", "vulkan-tools", "protontricks", "winetricks"])
    apt_install(["steam", "lutris", "dolphin-emu"])
    apt_install(["default-jre", "openjdk-21-jre", "openjdk-17-jre", "openjdk-8-jre"])

    add_user_to_groups(GAMING_USER_GROUPS)
    log_success("Ubuntu / Debian gaming suite installation complete.")


def install_games(distro: Optional[DistroType] = None) -> None:
    """Install gaming suite for the specified or detected distribution."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()

    if active_distro == DistroType.ARCH:
        install_games_arch()
    elif active_distro == DistroType.FEDORA:
        install_games_fedora()
    elif active_distro in (DistroType.UBUNTU, DistroType.DEBIAN):
        install_games_ubuntu()


if __name__ == "__main__":
    install_games()

