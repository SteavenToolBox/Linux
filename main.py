#!/usr/bin/env python3
"""SteavenToolBox for Linux - Main Entry Point.

This is the primary Python executable for SteavenToolBox.
Run directly without arguments for an interactive terminal interface:
    python3 main.py

Or use command-line flags for automated tasks:
    python3 main.py --update
    python3 main.py --games
    python3 main.py --apps
    python3 main.py --i3
    python3 main.py --sway
    python3 main.py --hyprland
    python3 main.py --drivers
    python3 main.py --distro fedora --apps
"""

import argparse
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from steaventoolbox.apps import install_apps
from steaventoolbox.core import DistroType, detect_distro, ensure_toolbox_dirs, log_info
from steaventoolbox.debloat import debloat_system
from steaventoolbox.drivers import install_gpu_drivers
from steaventoolbox.games import install_games
from steaventoolbox.gnome import install_gnome
from steaventoolbox.hyprland import install_hyprland
from steaventoolbox.i3 import install_i3
from steaventoolbox.kde import install_kde
from steaventoolbox.menu import run_menu_loop
from steaventoolbox.pacman import run_pacman_setup
from steaventoolbox.prerequisites import setup_prerequisites
from steaventoolbox.printer import install_printer
from steaventoolbox.steavensettings import install_steavensettings
from steaventoolbox.sway import install_sway
from steaventoolbox.update import install_topgrade, update_system


def parse_arguments() -> argparse.Namespace:
    """Configure command-line arguments using standard library argparse."""
    parser = argparse.ArgumentParser(
        description="SteavenToolBox for Linux - Python Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Run without options to start the interactive menu.",
    )
    parser.add_argument(
        "--distro",
        choices=["arch", "fedora", "ubuntu", "debian"],
        help="Override automatic distribution detection",
    )
    parser.add_argument("--update", action="store_true", help="Perform full system update (via Topgrade)")
    parser.add_argument("--topgrade", action="store_true", help="Install Topgrade for the target distribution")
    parser.add_argument("--debloat", action="store_true", help="Debloat unwanted pre-installed packages")
    parser.add_argument("--i3", action="store_true", help="Install i3 Window Manager setup")
    parser.add_argument("--sway", action="store_true", help="Install Sway Wayland Compositor setup")
    parser.add_argument("--hyprland", action="store_true", help="Install Hyprland Wayland Compositor setup")
    parser.add_argument("--games", action="store_true", help="Install Gaming utilities, launchers, and emulators")
    parser.add_argument("--apps", action="store_true", help="Install standard applications suite")
    parser.add_argument("--printer", action="store_true", help="Install printer drivers and CUPS service")
    parser.add_argument("--drivers", action="store_true", help="Auto-detect GPU and install drivers")
    parser.add_argument("--steavensettings", action="store_true", help="Install SteavenSettings optimizations")
    parser.add_argument("--gnome", action="store_true", help="Install GNOME Desktop (Arch)")
    parser.add_argument("--kde", action="store_true", help="Install KDE Plasma Desktop (Arch)")
    parser.add_argument("--optimize-pacman", action="store_true", help="Optimize pacman configuration (Arch)")

    return parser.parse_args()


def main() -> int:
    """Main program routine."""
    args = parse_arguments()

    # Determine distribution
    if args.distro:
        distro = DistroType(args.distro)
        log_info(f"Using forced distribution: {distro.display_name()}")
    else:
        distro = detect_distro()

    # Any non-interactive flag specified?
    flags_specified = any([
        args.update, args.topgrade, args.debloat, args.i3, args.sway, args.hyprland, args.games, args.apps,
        args.printer, args.drivers, args.steavensettings,
        args.gnome, args.kde, args.optimize_pacman
    ])

    if not flags_specified:
        # Launch interactive menu loop
        run_menu_loop(force_distro=distro)
        return 0

    # Execute specific flag routines
    ensure_toolbox_dirs()
    setup_prerequisites(distro)

    if args.topgrade:
        install_topgrade(distro)
    if args.update:
        update_system(distro)
    if args.i3:
        install_i3(distro)
    if args.sway:
        install_sway(distro)
    if args.hyprland:
        install_hyprland(distro)
    if args.games:
        install_games(distro)
    if args.apps:
        install_apps(distro)
    if args.printer:
        install_printer(distro)
    if args.drivers:
        install_gpu_drivers(distro)
    if args.steavensettings:
        install_steavensettings()
    if args.debloat:
        debloat_system(distro)
    if args.gnome:
        install_gnome(distro)
    if args.kde:
        install_kde(distro)
    if args.optimize_pacman:
        run_pacman_setup(distro)

    return 0


if __name__ == "__main__":
    sys.exit(main())
