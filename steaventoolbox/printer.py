"""Printer Drivers and CUPS Installation Module.

Installs CUPS printing subsystem, HP Linux Imaging and Printing (HPLIP),
Gutenprint, Epson drivers, Foomatic databases, and GUI printer managers across:
- Arch Linux
- Fedora Linux
- Ubuntu & Debian
"""

from typing import Optional

from steaventoolbox.core import (
    DistroType,
    add_user_to_groups,
    apt_install,
    detect_distro,
    dnf_install,
    ensure_toolbox_dirs,
    log_header,
    log_success,
    pacman_install,
    run_cmd,
)


def install_printer_arch() -> None:
    """Install CUPS and printer drivers on Arch Linux."""
    log_header("Installing Printer Drivers (Arch Linux)")

    pacman_install([
        "cups", "cups-browsed", "foomatic-db-engine", "foomatic-db",
        "foomatic-db-ppds", "foomatic-db-nonfree", "foomatic-db-nonfree-ppds",
        "gutenprint", "foomatic-db-gutenprint-ppds", "hplip",
        "epson-inkjet-printer-escpr", "epson-inkjet-printer-escpr2",
        "system-config-printer", "ipp-usb", "sane-airscan", "python-pyqt5"
    ])

    run_cmd(["systemctl", "enable", "--now", "cups"], sudo=True, check=False)
    run_cmd(["systemctl", "enable", "--now", "cups-browsed"], sudo=True, check=False)
    add_user_to_groups(["lp"])
    log_success("Arch Linux printer drivers and services enabled.")


def install_printer_fedora() -> None:
    """Install CUPS and printer drivers on Fedora."""
    log_header("Installing Printer Drivers (Fedora)")

    dnf_install([
        "cups", "foomatic-db", "foomatic-db-ppds", "gutenprint", "hplip",
        "epson-inkjet-printer-escpr", "epson-inkjet-printer-escpr2", "system-config-printer"
    ])

    run_cmd(["systemctl", "enable", "--now", "cups"], sudo=True, check=False)
    add_user_to_groups(["lp"])
    log_success("Fedora printer drivers and services enabled.")


def install_printer_ubuntu() -> None:
    """Install CUPS and printer drivers on Ubuntu / Debian."""
    log_header("Installing Printer Drivers (Ubuntu / Debian)")

    apt_install([
        "cups", "foomatic-db-engine", "foomatic-db", "hplip", "system-config-printer"
    ])

    run_cmd(["systemctl", "enable", "--now", "cups"], sudo=True, check=False)
    add_user_to_groups(["lp"])
    log_success("Ubuntu / Debian printer drivers and services enabled.")


def install_printer(distro: Optional[DistroType] = None) -> None:
    """Install printer drivers and services for the specified or detected distribution."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()

    if active_distro == DistroType.ARCH:
        install_printer_arch()
    elif active_distro == DistroType.FEDORA:
        install_printer_fedora()
    elif active_distro in (DistroType.UBUNTU, DistroType.DEBIAN):
        install_printer_ubuntu()


if __name__ == "__main__":
    install_printer()

