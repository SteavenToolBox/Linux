"""Core utilities for SteavenToolBox.

This module provides common helper functions used across the toolbox:
- Distribution detection (reading and parsing /etc/os-release)
- Subprocess execution with formatted logs and error handling
- Package installation wrappers for pacman, yay/paru, dnf, copr, and apt
- User and group management
- Temporary directory initialization
"""

import getpass
import os
import shutil
import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

# Global tracking for active temp directory
_ACTIVE_TMP_DIR: Path = Path("/tmp/steaventoolbox/tmp")


class Colors:
    """ANSI color codes for styling terminal output."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


class DistroType(str, Enum):
    """Enumeration representing supported Linux distributions."""
    ARCH = "arch"
    FEDORA = "fedora"
    UBUNTU = "ubuntu"
    DEBIAN = "debian"
    UNKNOWN = "unknown"

    def display_name(self) -> str:
        """Return a human-readable name for the distribution."""
        names = {
            DistroType.ARCH: "Arch Linux",
            DistroType.FEDORA: "Fedora Linux",
            DistroType.UBUNTU: "Ubuntu Linux",
            DistroType.DEBIAN: "Debian GNU/Linux",
            DistroType.UNKNOWN: "Unknown Distribution",
        }
        return names.get(self, "Unknown Distribution")


def log_info(message: str) -> None:
    """Print an informational message in cyan."""
    print(f"{Colors.CYAN}[INFO]{Colors.RESET} {message}")


def log_success(message: str) -> None:
    """Print a success message in green."""
    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {message}")


def log_warning(message: str) -> None:
    """Print a warning message in yellow."""
    print(f"{Colors.YELLOW}[WARNING]{Colors.RESET} {message}")


def log_error(message: str) -> None:
    """Print an error message in bold red."""
    print(f"{Colors.RED}{Colors.BOLD}[ERROR]{Colors.RESET} {message}")


def log_header(title: str) -> None:
    """Print a formatted section banner."""
    separator = "=" * 60
    print(f"\n{Colors.BLUE}{Colors.BOLD}{separator}")
    print(f" {title}")
    print(f"{separator}{Colors.RESET}\n")


def get_real_user() -> str:
    """Get the original non-root username even when script is run with sudo.

    When running with `sudo python3 ...`, `os.getlogin()` or `getpass.getuser()`
    often returns 'root'. In Linux, the original invoking user is stored in
    the 'SUDO_USER' environment variable.
    """
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        return sudo_user
    try:
        return os.getlogin()
    except OSError:
        return getpass.getuser()


def detect_distro() -> DistroType:
    """Detect the current Linux distribution by reading /etc/os-release.

    Returns:
        DistroType: The detected distribution enum value.
    """
    os_release_path = Path("/etc/os-release")
    if not os_release_path.exists():
        log_warning("/etc/os-release not found. Distribution could not be determined.")
        return DistroType.UNKNOWN

    try:
        content = os_release_path.read_text(encoding="utf-8").lower()
        if "arch" in content or "cachyos" in content or "manjaro" in content or "endeavouros" in content:
            return DistroType.ARCH
        if "fedora" in content:
            return DistroType.FEDORA
        if "ubuntu" in content or "pop" in content or "linuxmint" in content:
            return DistroType.UBUNTU
        if "debian" in content:
            return DistroType.DEBIAN
    except Exception as exc:
        log_error(f"Failed to read /etc/os-release: {exc}")

    return DistroType.UNKNOWN


def run_cmd(
    cmd: Union[List[str], str],
    check: bool = True,
    shell: bool = False,
    sudo: bool = False,
    capture_output: bool = False,
) -> subprocess.CompletedProcess:
    """Execute a system command safely using subprocess.run.

    Args:
        cmd: List of command arguments or string if shell=True.
        check: If True, raises CalledProcessError if return code is non-zero.
        shell: If True, runs through the shell.
        sudo: If True and current user is not root, prefixes command with sudo.
        capture_output: If True, captures stdout and stderr instead of streaming.

    Returns:
        subprocess.CompletedProcess: The finished process details.
    """
    if sudo and os.geteuid() != 0:
        if isinstance(cmd, list):
            if cmd and cmd[0] != "sudo":
                cmd = ["sudo"] + cmd
        elif isinstance(cmd, str):
            if not cmd.strip().startswith("sudo"):
                cmd = f"sudo {cmd}"

    cmd_display = " ".join(cmd) if isinstance(cmd, list) else cmd
    log_info(f"Executing: {cmd_display}")

    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            check=check,
            capture_output=capture_output,
            text=True,
        )
        return result
    except subprocess.CalledProcessError as err:
        log_error(f"Command failed with exit code {err.returncode}: {cmd_display}")
        if not check:
            return err  # type: ignore
        raise err


def is_tool_installed(tool_name: str) -> bool:
    """Check if an executable exists in the system's PATH."""
    return shutil.which(tool_name) is not None


def get_tmp_dir() -> Path:
    """Return the currently configured temporary directory path."""
    return _ACTIVE_TMP_DIR


def ensure_toolbox_dirs(toolbox_dir: Path = Path("/steaventoolbox")) -> Path:
    """Ensure toolbox working directory and tmp cache exist with permissions."""
    global _ACTIVE_TMP_DIR
    tmp_dir = toolbox_dir / "tmp"
    try:
        res = run_cmd(["mkdir", "-p", str(tmp_dir)], sudo=True, check=False)
        if res.returncode == 0:
            run_cmd(["chmod", "-R", "777", str(toolbox_dir)], sudo=True, check=False)
            run_cmd(f"rm -rf {tmp_dir}/*", shell=True, sudo=True, check=False)
            log_success(f"Toolbox workspace initialized at {tmp_dir}")
            _ACTIVE_TMP_DIR = tmp_dir
            return tmp_dir
    except Exception as exc:
        log_warning(f"Could not initialize {toolbox_dir}: {exc}")

    fallback_tmp = Path("/tmp/steaventoolbox/tmp")
    fallback_tmp.mkdir(parents=True, exist_ok=True)
    log_info(f"Using fallback temporary workspace at {fallback_tmp}")
    _ACTIVE_TMP_DIR = fallback_tmp
    return fallback_tmp


def add_user_to_groups(groups: List[str], username: Optional[str] = None) -> None:
    """Add a user to a list of system groups."""
    user = username or get_real_user()
    if not user or user == "root":
        log_warning("Target user is root or not identified; skipping group assignment.")
        return

    group_str = ",".join(groups)
    log_info(f"Adding user '{user}' to groups: {group_str}")
    run_cmd(["usermod", "-a", "-G", group_str, user], sudo=True, check=False)


# Universal package installation helpers
def pacman_install(packages: List[str]) -> None:
    """Install packages using pacman (Arch Linux)."""
    log_info(f"Pacman installing: {' '.join(packages)}")
    run_cmd(["pacman", "-S", "--noconfirm", "--needed"] + packages, sudo=True, check=False)


def aur_install(packages: List[str]) -> None:
    """Install AUR packages using yay or paru (Arch Linux)."""
    aur_helper = "yay" if is_tool_installed("yay") else ("paru" if is_tool_installed("paru") else None)
    if not aur_helper:
        log_warning(f"No AUR helper found. Skipping AUR packages: {' '.join(packages)}")
        return
    log_info(f"{aur_helper} installing: {' '.join(packages)}")
    run_cmd([aur_helper, "-S", "--noconfirm", "--needed"] + packages, check=False)


def dnf_install(packages: List[str]) -> None:
    """Install packages using dnf (Fedora)."""
    log_info(f"DNF installing: {' '.join(packages)}")
    run_cmd(["dnf", "install", "-y"] + packages, sudo=True, check=False)


def enable_copr(repo: str) -> None:
    """Enable a COPR repository (Fedora)."""
    log_info(f"Enabling COPR: {repo}")
    run_cmd(["dnf", "copr", "enable", "-y", repo], sudo=True, check=False)


def apt_install(packages: List[str]) -> None:
    """Install packages using apt (Ubuntu / Debian)."""
    log_info(f"APT installing: {' '.join(packages)}")
    run_cmd(["apt", "install", "-y"] + packages, sudo=True, check=False)
