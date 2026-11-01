"""System Update and Topgrade Installation Module.

Installs Topgrade across distributions:
- Fedora: COPR lilay/topgrade (sudo dnf copr enable lilay/topgrade && sudo dnf install topgrade)
- Arch Linux: AUR package topgrade-bin (https://aur.archlinux.org/packages/topgrade-bin)
- Ubuntu / Debian: deb-get (deb-get install topgrade)

Always installs Topgrade and executes system updates using Topgrade.
"""

from typing import Optional

from steaventoolbox.core import (
    DistroType,
    apt_install,
    aur_install,
    detect_distro,
    dnf_install,
    enable_copr,
    ensure_toolbox_dirs,
    is_tool_installed,
    log_header,
    log_info,
    log_success,
    log_warning,
    run_cmd,
)


def install_topgrade_arch() -> None:
    """Install topgrade-bin via AUR on Arch Linux."""
    log_info("Installing topgrade-bin from AUR on Arch Linux...")
    aur_install(["topgrade-bin"])


def install_topgrade_fedora() -> None:
    """Install topgrade on Fedora via COPR repository lilay/topgrade."""
    log_info("Enabling lilay/topgrade COPR repository on Fedora...")
    run_cmd(["dnf", "install", "-y", "dnf-command(copr)"], sudo=True, check=False)
    enable_copr("lilay/topgrade")
    log_info("Installing topgrade via dnf...")
    dnf_install(["topgrade"])


def install_topgrade_github_release() -> bool:
    """Download and install the latest Topgrade release from GitHub (deb or binary)."""
    import json
    import urllib.request
    from steaventoolbox.core import get_tmp_dir

    log_info("Querying latest release from github.com/topgrade-rs/topgrade/releases/latest...")
    api_url = "https://api.github.com/repos/topgrade-rs/topgrade/releases/latest"
    headers = {"User-Agent": "SteavenToolBox"}

    data = None
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        log_warning(f"Could not reach GitHub API ({exc}). Using direct download fallback.")

    deb_url = None
    tar_url = None

    if data and "assets" in data:
        for asset in data["assets"]:
            name = asset.get("name", "").lower()
            url = asset.get("browser_download_url")
            if name.endswith(".deb") and ("amd64" in name or "x86_64" in name):
                deb_url = url
                break
            elif name.endswith(".deb"):
                deb_url = url
            elif "x86_64" in name and "linux" in name and name.endswith(".tar.gz"):
                tar_url = url

    # 1. Attempt installing .deb package if available
    if deb_url:
        log_info(f"Found Topgrade deb release: {deb_url}")
        tmp_deb = get_tmp_dir() / "topgrade_latest.deb"
        run_cmd(["curl", "-sL", deb_url, "-o", str(tmp_deb)], check=False)
        if tmp_deb.exists() and tmp_deb.stat().st_size > 0:
            log_info("Installing downloaded Topgrade .deb package...")
            run_cmd(["dpkg", "-i", str(tmp_deb)], sudo=True, check=False)
            run_cmd(["apt", "install", "-f", "-y"], sudo=True, check=False)
            tmp_deb.unlink(missing_ok=True)
            if is_tool_installed("topgrade"):
                log_success("Topgrade installed successfully from GitHub .deb release.")
                return True

    # 2. Fallback to downloading and extracting the pre-compiled Linux x86_64 archive
    if not tar_url:
        tar_url = "https://github.com/topgrade-rs/topgrade/releases/latest/download/topgrade-x86_64-unknown-linux-gnu.tar.gz"

    log_info(f"Downloading Topgrade release binary: {tar_url}")
    tmp_tar = get_tmp_dir() / "topgrade.tar.gz"
    run_cmd(["curl", "-sL", tar_url, "-o", str(tmp_tar)], check=False)

    if tmp_tar.exists() and tmp_tar.stat().st_size > 0:
        extract_dir = get_tmp_dir() / "topgrade_extract"
        extract_dir.mkdir(parents=True, exist_ok=True)
        run_cmd(["tar", "-xzf", str(tmp_tar), "-C", str(extract_dir)], check=False)
        topgrade_bin = extract_dir / "topgrade"
        if topgrade_bin.exists():
            run_cmd(["chmod", "+x", str(topgrade_bin)])
            run_cmd(["cp", str(topgrade_bin), "/usr/local/bin/topgrade"], sudo=True, check=False)
            log_success("Topgrade installed successfully to /usr/local/bin/topgrade.")
            return True

    return False


def install_topgrade_ubuntu() -> None:
    """Install topgrade on Ubuntu/Debian using deb-get with GitHub release fallback."""
    log_info("Attempting to install Topgrade via deb-get on Ubuntu/Debian...")

    # Ensure required dependencies for deb-get (lsb-release, curl, wget) are installed
    required_packages = []
    if not is_tool_installed("lsb_release"):
        required_packages.append("lsb-release")
    if not is_tool_installed("curl"):
        required_packages.append("curl")
    if not is_tool_installed("wget"):
        required_packages.append("wget")

    if required_packages:
        log_info(f"Installing required deb-get dependencies: {' '.join(required_packages)}...")
        apt_install(required_packages)

    deb_get_available = is_tool_installed("deb-get")
    if not deb_get_available:
        log_info("deb-get not found. Installing deb-get...")
        res = run_cmd(
            "curl -sL https://raw.githubusercontent.com/wimpysworld/deb-get/main/deb-get | sudo bash -s install deb-get",
            shell=True,
            check=False,
        )
        deb_get_available = res.returncode == 0 and is_tool_installed("deb-get")

    installed = False
    if deb_get_available:
        log_info("Running 'deb-get install topgrade'...")
        install_res = run_cmd(["deb-get", "install", "topgrade"], sudo=True, check=False)
        if install_res.returncode == 0 and is_tool_installed("topgrade"):
            log_success("Topgrade installed via deb-get.")
            installed = True

    if not installed and not is_tool_installed("topgrade"):
        log_warning("deb-get failed or distribution not supported by deb-get (e.g. Debian Trixie).")
        log_info("Downloading latest Topgrade release from github.com/topgrade-rs/topgrade/releases/latest...")
        install_topgrade_github_release()


def install_topgrade(distro: Optional[DistroType] = None) -> None:
    """Install Topgrade according to distribution-specific sources."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()
    log_header(f"Installing Topgrade ({active_distro.display_name()})")

    if active_distro == DistroType.ARCH:
        install_topgrade_arch()
    elif active_distro == DistroType.FEDORA:
        install_topgrade_fedora()
    elif active_distro in (DistroType.UBUNTU, DistroType.DEBIAN):
        install_topgrade_ubuntu()
    else:
        log_warning(f"Topgrade automated installation not implemented for {active_distro.value}.")


def update_system(distro: Optional[DistroType] = None) -> None:
    """Always install Topgrade and perform full system update using Topgrade."""
    active_distro = distro or detect_distro()
    ensure_toolbox_dirs()
    log_header(f"Updating System ({active_distro.display_name()})")

    # Always ensure Topgrade is installed first
    if not is_tool_installed("topgrade"):
        log_info("Topgrade is not installed. Installing Topgrade...")
        install_topgrade(active_distro)

    # Always update using Topgrade
    log_info("Running Topgrade system update...")
    run_cmd(["topgrade"], check=False)
    log_success("System update finished.")


if __name__ == "__main__":
    update_system()
