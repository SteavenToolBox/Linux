"""Arch Linux Pacman Optimization and Repository Module.

Configures optimized pacman settings, downloads keys, and configures:
- Parallel downloads and ILoveCandy animation
- CachyOS optimized kernel and v3/v4 x86-64 repositories
- Chaotic-AUR pre-compiled repository
"""

from pathlib import Path
from typing import Optional

from steaventoolbox.core import (
    DistroType,
    detect_distro,
    ensure_toolbox_dirs,
    log_header,
    log_info,
    log_success,
    log_warning,
    pacman_install,
    run_cmd,
)

OPTIMIZED_PACMAN_CONF = """# /etc/pacman.conf
# SteavenToolBox Optimized Configuration

[options]
HoldPkg     = pacman glibc
Architecture = auto

# Visual and speed tweaks
Color
CheckSpace
ParallelDownloads = 5
DownloadUser = alpm
ILoveCandy

SigLevel    = Required DatabaseOptional
LocalFileSigLevel = Optional

# --- REPOSITORIES ---

# CachyOS Repositories
[cachyos-v3]
Include = /etc/pacman.d/cachyos-v3-mirrorlist
[cachyos-core-v3]
Include = /etc/pacman.d/cachyos-v3-mirrorlist
[cachyos-extra-v3]
Include = /etc/pacman.d/cachyos-v3-mirrorlist
[cachyos]
Include = /etc/pacman.d/cachyos-mirrorlist

# Official Arch Linux Repositories
[core]
Include = /etc/pacman.d/mirrorlist
[extra]
Include = /etc/pacman.d/mirrorlist
[multilib]
Include = /etc/pacman.d/mirrorlist

# Chaotic-AUR Repository
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist
"""


def optimize_pacman() -> None:
    """Optimize pacman configuration with CachyOS and Chaotic-AUR mirrors."""
    log_header("Optimizing Pacman Configuration")

    log_info("Importing repository signing keys...")
    run_cmd([
        "pacman-key", "--keyserver", "keyserver.ubuntu.com",
        "--recv-keys", "F3B607488DB35A47", "3056513887B78AEB"
    ], sudo=True, check=False)
    run_cmd([
        "pacman-key", "--lsign-key", "F3B607488DB35A47", "3056513887B78AEB"
    ], sudo=True, check=False)

    log_info("Installing CachyOS and Chaotic-AUR keyrings and mirrorlists...")
    keyring_urls = [
        "https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-keyring-20240331-1-any.pkg.tar.zst",
        "https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-mirrorlist-18-1-any.pkg.tar.zst",
        "https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-v3-mirrorlist-18-1-any.pkg.tar.zst",
        "https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-v4-mirrorlist-6-1-any.pkg.tar.zst",
        "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst",
        "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst",
    ]
    run_cmd(["pacman", "-U", "--noconfirm", "--needed"] + keyring_urls, sudo=True, check=False)

    # Backup existing /etc/pacman.conf
    pacman_conf = Path("/etc/pacman.conf")
    if pacman_conf.exists():
        backup_idx = 1
        while Path(f"/etc/pacman.conf.backup{backup_idx}").exists():
            backup_idx += 1
        backup_path = f"/etc/pacman.conf.backup{backup_idx}"
        log_info(f"Backing up /etc/pacman.conf to {backup_path}")
        run_cmd(["cp", str(pacman_conf), backup_path], sudo=True, check=False)

    # Write optimized configuration directly
    tmp_conf = Path("/tmp/pacman.conf.steaven")
    tmp_conf.write_text(OPTIMIZED_PACMAN_CONF, encoding="utf-8")
    run_cmd(["cp", str(tmp_conf), "/etc/pacman.conf"], sudo=True, check=False)
    tmp_conf.unlink(missing_ok=True)

    log_success("Pacman configuration optimized successfully.")


def run_pacman_setup(distro: Optional[DistroType] = None) -> None:
    """Run pacman optimization if target distro is Arch Linux."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()

    if active_distro == DistroType.ARCH:
        optimize_pacman()
    else:
        log_warning("Pacman optimization is only available on Arch Linux.")


if __name__ == "__main__":
    run_pacman_setup()

