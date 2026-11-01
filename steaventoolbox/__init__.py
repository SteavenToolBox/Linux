"""SteavenToolBox for Linux - Python Edition.

A modular, cross-distribution Linux setup and post-installation toolbox
for Arch Linux, Fedora, Ubuntu, and Debian.

Every application, tool, and setup routine is maintained in its own dedicated module.
"""

from steaventoolbox.apps import install_apps
from steaventoolbox.core import DistroType, detect_distro, run_cmd
from steaventoolbox.debloat import debloat_system
from steaventoolbox.drivers import detect_gpus, install_gpu_drivers
from steaventoolbox.games import install_games
from steaventoolbox.gnome import install_gnome
from steaventoolbox.hyprland import install_hyprland
from steaventoolbox.i3 import install_i3
from steaventoolbox.kde import install_kde
from steaventoolbox.pacman import optimize_pacman
from steaventoolbox.printer import install_printer
from steaventoolbox.steavensettings import install_steavensettings
from steaventoolbox.sway import install_sway
from steaventoolbox.update import install_topgrade, update_system

__version__ = "2.0.0"
__author__ = "SteavenToolBox Team & Python Student Contributor"

__all__ = [
    "DistroType",
    "detect_distro",
    "run_cmd",
    "install_apps",
    "install_games",
    "install_i3",
    "install_sway",
    "install_printer",
    "install_gpu_drivers",
    "detect_gpus",
    "install_steavensettings",
    "debloat_system",
    "install_gnome",
    "install_kde",
    "install_hyprland",
    "optimize_pacman",
    "update_system",
    "install_topgrade",
    "__version__",
]
