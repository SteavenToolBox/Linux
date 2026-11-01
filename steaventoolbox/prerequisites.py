"""Prerequisites checking and configuration module.

Ensures essential tools and repositories exist on Arch, Fedora, Ubuntu, and Debian:
- wget and git on all distros
- yay AUR helper on Arch
- RPM Fusion repositories and @core updates on Fedora
- i386 32-bit architecture on Ubuntu and Debian
"""

from typing import Optional

from steaventoolbox.core import (
    DistroType,
    aur_install,
    detect_distro,
    ensure_toolbox_dirs,
    get_tmp_dir,
    is_tool_installed,
    log_header,
    log_info,
    log_warning,
    run_cmd,
)


def setup_arch_prerequisites() -> None:
    """Ensure wget, git, yay, and topgrade are installed on Arch."""
    log_header("Arch Linux Prerequisites Check")

    if not is_tool_installed("wget"):
        log_info("Installing wget...")
        run_cmd(["pacman", "-Syu", "--noconfirm", "--needed", "wget"], sudo=True, check=False)

    if not is_tool_installed("git"):
        log_info("Installing git...")
        run_cmd(["pacman", "-Syu", "--noconfirm", "--needed", "git"], sudo=True, check=False)

    if not is_tool_installed("yay"):
        log_info("yay AUR helper not found. Building and installing yay-bin...")
        run_cmd(["pacman", "-Syu", "--noconfirm", "--needed", "git", "base-devel"], sudo=True, check=False)
        tmp_dir = get_tmp_dir() / "yay-bin"
        if tmp_dir.exists():
            run_cmd(f"rm -rf {tmp_dir}", shell=True, sudo=True, check=False)
        clone_res = run_cmd(["git", "clone", "https://aur.archlinux.org/yay-bin.git", str(tmp_dir)], check=False)
        if clone_res.returncode == 0:
            run_cmd(f"cd {tmp_dir} && makepkg -si --noconfirm", shell=True, check=False)
        else:
            log_warning("Could not clone yay-bin repository.")
    else:
        log_info("yay is already installed.")


def setup_fedora_prerequisites() -> None:
    """Ensure wget, git, and RPM Fusion are configured on Fedora."""
    log_header("Fedora Prerequisites Check")

    if not is_tool_installed("wget"):
        run_cmd(["dnf", "install", "-y", "wget"], sudo=True, check=False)

    if not is_tool_installed("git"):
        run_cmd(["dnf", "install", "-y", "git"], sudo=True, check=False)

    check_fusion = run_cmd(
        "dnf list installed rpmfusion-free-release rpmfusion-nonfree-release",
        shell=True,
        sudo=True,
        capture_output=True,
        check=False,
    )
    if check_fusion.returncode != 0:
        log_info("Installing RPM Fusion repositories...")
        fusion_cmd = (
            "dnf install -y "
            "https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm "
            "https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm"
        )
        run_cmd(fusion_cmd, shell=True, sudo=True, check=False)

    run_cmd(r"dnf install -y rpmfusion-\*-appstream-data", shell=True, sudo=True, check=False)


def setup_ubuntu_prerequisites() -> None:
    """Ensure wget, git, curl, lsb-release, and i386 architecture are enabled on Ubuntu/Debian."""
    log_header("Ubuntu/Debian Prerequisites Check")

    pkgs_to_install = []
    if not is_tool_installed("wget"):
        pkgs_to_install.append("wget")
    if not is_tool_installed("git"):
        pkgs_to_install.append("git")
    if not is_tool_installed("curl"):
        pkgs_to_install.append("curl")
    if not is_tool_installed("lsb_release"):
        pkgs_to_install.append("lsb-release")

    if pkgs_to_install:
        run_cmd(["apt", "install", "-y"] + pkgs_to_install, sudo=True, check=False)

    res = run_cmd("dpkg --print-foreign-architectures", shell=True, capture_output=True, check=False)
    if "i386" not in res.stdout:
        log_info("Enabling i386 32-bit architecture...")
        run_cmd(["dpkg", "--add-architecture", "i386"], sudo=True, check=False)
        run_cmd(["apt", "update"], sudo=True, check=False)


def setup_prerequisites(distro: Optional[DistroType] = None) -> None:
    """Unified entry point to setup prerequisites for the detected distribution."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()

    if active_distro == DistroType.ARCH:
        setup_arch_prerequisites()
    elif active_distro == DistroType.FEDORA:
        setup_fedora_prerequisites()
    elif active_distro in (DistroType.UBUNTU, DistroType.DEBIAN):
        setup_ubuntu_prerequisites()


if __name__ == "__main__":
    setup_prerequisites()

