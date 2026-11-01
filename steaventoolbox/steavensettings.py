"""SteavenSettings Optimization Module.

Clones and installs SteavenSettings repository (system tweaks and Nvidia fixes).
"""

from pathlib import Path

from steaventoolbox.core import (
    ensure_toolbox_dirs,
    get_tmp_dir,
    log_header,
    log_info,
    log_success,
    log_warning,
    run_cmd,
)


def install_steavensettings() -> None:
    """Clone and install SteavenSettings optimizations repository."""
    ensure_toolbox_dirs()
    log_header("Installing SteavenSettings")
    target_dir = get_tmp_dir() / "steavensettings"

    if target_dir.exists():
        run_cmd(f"rm -rf {target_dir}", shell=True, sudo=True, check=False)

    log_info("Cloning SteavenSettings repository...")
    run_cmd([
        "git", "clone",
        "https://github.com/SteavenGamerYT/SteavenSettings",
        str(target_dir)
    ], sudo=True, check=False)

    install_script = target_dir / "install.sh"
    if install_script.exists():
        log_info("Running SteavenSettings installer...")
        run_cmd(f"cd {target_dir} && ./install.sh", shell=True, sudo=True, check=False)
        log_success("SteavenSettings installed successfully.")
    else:
        log_warning("install.sh not found inside cloned repository.")


if __name__ == "__main__":
    install_steavensettings()

