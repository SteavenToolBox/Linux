"""Interactive CLI Menu for SteavenToolBox.

Displays an interactive, colored terminal menu allowing users to select
installation options, system updates, driver installations, and system maintenance.
Each app and tool is maintained in its own dedicated module.
"""

from typing import Optional

from steaventoolbox.apps import install_apps
from steaventoolbox.core import (
    Colors,
    DistroType,
    detect_distro,
    ensure_toolbox_dirs,
    log_error,
    log_info,
    log_warning,
)
from steaventoolbox.debloat import debloat_system
from steaventoolbox.drivers import install_gpu_drivers
from steaventoolbox.games import install_games
from steaventoolbox.gnome import install_gnome
from steaventoolbox.hyprland import install_hyprland
from steaventoolbox.i3 import install_i3
from steaventoolbox.kde import install_kde
from steaventoolbox.pacman import run_pacman_setup
from steaventoolbox.prerequisites import setup_prerequisites
from steaventoolbox.printer import install_printer
from steaventoolbox.steavensettings import install_steavensettings
from steaventoolbox.sway import install_sway
from steaventoolbox.update import update_system


def show_banner(distro: DistroType) -> None:
    """Display the SteavenToolBox header banner."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}========================================================")
    print(" SteavenToolBox-For-Linux | We care about your pc! Linux!")
    print(f" Detected OS: {distro.display_name()}")
    print(f"========================================================{Colors.RESET}")


def show_menu() -> None:
    """Print the numbered menu options to the terminal."""
    print(f"{Colors.GREEN} 1.{Colors.RESET} Update Linux")
    print(f"{Colors.GREEN} 2.{Colors.RESET} Debloat Linux")
    print(f"{Colors.GREEN} 3.{Colors.RESET} Install i3 Window Manager")
    print(f"{Colors.GREEN} 4.{Colors.RESET} Install Sway Wayland Compositor")
    print(f"{Colors.GREEN} 5.{Colors.RESET} Install Games Suite & Emulators")
    print(f"{Colors.GREEN} 6.{Colors.RESET} Install Applications & Disks Suite")
    print(f"{Colors.GREEN} 7.{Colors.RESET} Install Printer Drivers (CUPS)")
    print(f"{Colors.GREEN} 8.{Colors.RESET} Install GPU Drivers (Auto-detects Nvidia/Intel/AMD)")
    print(f"{Colors.GREEN} 9.{Colors.RESET} Install SteavenSettings (Includes Nvidia driver fixes)")
    print(f"{Colors.YELLOW}10.{Colors.RESET} Install Hyprland Compositor")
    print(f"{Colors.YELLOW}11.{Colors.RESET} Install Desktop Environment (GNOME / KDE)")
    print(f"{Colors.YELLOW}12.{Colors.RESET} Optimize Pacman & Repositories [Arch]")
    print(f"{Colors.RED} 0.{Colors.RESET} Exit")


def handle_desktop_environment_menu(distro: DistroType) -> None:
    """Handle submenu for installing GNOME or KDE."""
    print("\nDesktop Environments:")
    print("1. GNOME")
    print("2. KDE Plasma")
    print("0. Back to Main Menu")
    choice = input("\nSelect desktop environment [1-2, 0]: ").strip()

    if choice == "1":
        install_gnome(distro)
    elif choice == "2":
        install_kde(distro)
    elif choice == "0":
        return
    else:
        print("Invalid choice.")


def run_menu_loop(force_distro: Optional[DistroType] = None) -> None:
    """Run the main interactive menu event loop."""
    distro = force_distro or detect_distro()
    ensure_toolbox_dirs()
    setup_prerequisites(distro)

    while True:
        try:
            show_banner(distro)
            show_menu()
            choice = input(f"\n{Colors.BOLD}Select an option [0-12]: {Colors.RESET}").strip()

            if choice in ("0", "exit", "quit", "q"):
                log_info("Exiting SteavenToolBox. Happy Linux computing!")
                break

            elif choice == "1":
                update_system(distro)

            elif choice == "2":
                debloat_system(distro)

            elif choice == "3":
                install_i3(distro)

            elif choice == "4":
                install_sway(distro)

            elif choice == "5":
                install_games(distro)

            elif choice == "6":
                install_apps(distro)

            elif choice == "7":
                install_printer(distro)

            elif choice == "8":
                install_gpu_drivers(distro)

            elif choice == "":
                install_steavensettings()

            elif choice == "10":
                install_hyprland(distro)

            elif choice == "11":
                handle_desktop_environment_menu(distro)

            elif choice == "12":
                run_pacman_setup(distro)

            else:
                log_warning(f"Invalid option: '{choice}'. Please select a valid number.")

            input(f"\n{Colors.CYAN}Press Enter to return to the menu...{Colors.RESET}")

        except KeyboardInterrupt:
            print("\n")
            log_info("Process interrupted by user (Ctrl+C). Exiting...")
            break
        except Exception as err:
            log_error(f"An unexpected error occurred: {err}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")


if __name__ == "__main__":
    run_menu_loop()
