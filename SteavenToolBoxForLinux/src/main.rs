use std::process::Command;

fn main() {
    let mut run = 1; // run flag

    // Check if wget is installed or not
    let wget_check = Command::new("sh")
        .arg("-c")
        .arg("command -v wget")
        .output()
        .expect("Failed to check if wget is installed.");

    if !wget_check.stdout.is_empty() {
        println!("wget is already installed.");
    } else {
        println!("wget could not be found, installing it.");
        let distro = std::fs::read_to_string("/etc/os-release").expect("Failed to read os-release file.");
        let package_manager = if distro.contains("Arch") {
            "pacman"
        } else if distro.contains("Ubuntu") {
            "apt"
        } else if distro.contains("Fedora") {
            "dnf"
        } else if distro.contains("Debian") {
            "apt"
        } else {
            panic!("Unsupported distribution.");
        };
        let mut install_command = match package_manager {
            "pacman" => {
                let mut cmd = Command::new("sudo");
                cmd.arg("pacman").arg("-Syu").arg("--noconfirm").arg("--needed").arg("wget");
                cmd
            }
            "apt" => {
                let mut cmd = Command::new("sudo");
                cmd.arg("apt").arg("install").arg("-y").arg("wget");
                cmd
            }
            "dnf" => {
                let mut cmd = Command::new("sudo");
                cmd.arg("dnf").arg("install").arg("-y").arg("wget");
                cmd
            }
            _ => panic!("Unsupported package manager."),
        };

        install_command.status().expect("Failed to install wget.");
    }

    // Check if yay is installed or not
    let distro = std::fs::read_to_string("/etc/os-release").expect("Failed to read os-release file.");
    if distro.contains("Arch") {
        let yay_check = Command::new("sh")
            .arg("-c")
            .arg("command -v yay")
            .output()
            .expect("Failed to check if yay is installed.");

        if !yay_check.stdout.is_empty() {
            println!("yay is already installed.");
        } else {
            println!("yay could not be found, installing it.");
            Command::new("sudo")
                .arg("pacman")
                .arg("-Syu")
                .arg("--noconfirm")
                .arg("--needed")
                .arg("git")
                .arg("base-devel")
                .status()
                .expect("Failed to install yay.");
            Command::new("git")
                .arg("clone")
                .arg("https://aur.archlinux.org/yay-bin.git")
                .status()
                .expect("Failed to clone yay repository.");
            Command::new("sh")
                .arg("-c")
                .arg("cd yay-bin/ && makepkg -si --noconfirm")
                .status()
                .expect("Failed to change directory to yay-bin and run makepkg.");
            }
        } else {
            println!("Aur is not supported on this distribution.");
        }
    
    // Check if topgrade is installed or not
    if distro.contains("Arch") {
        let topgrade_check = Command::new("sh")
            .arg("-c")
            .arg("command -v topgrade")
            .output()
            .expect("Failed to check if topgrade is installed.");

        if !topgrade_check.stdout.is_empty() {
            println!("topgrade is already installed.");
        } else {
            println!("topgrade could not be found, installing it.");
            Command::new("yay")
                .arg("-Syu")
                .arg("--noconfirm")
                .arg("--needed")
                .arg("topgrade")
                .status()
                .expect("Failed to install topgrade.");
        }
    } else {
        println!("Topgrade is not supported on this distribution.");
    }

    while run == 1 {
        println!("=============================================================");
        println!("SteavenToolbox-For-Linux | We care about your pc! Arch Linux!");
        println!("=============================================================");
        println!("1. Update Linux");
        println!("2. Install Core Linux Packages required for any desktop environment / window manager");
        println!("3. Install Gnome");
        println!("4. Install Kde");
        println!("5. Install i3");
        println!("6. Install Hyprland");
        println!("7. Install Nvidia Beta Drivers for explict sync");
        println!("8. Install SteavenSettings Incloudes Settings that fixs nvidia beta drivers as well");
        println!("9. Install SteavenGamerYT Dot Files, backup your old dot files, this will delete your current ones");
        println!("0. Exit");

        let mut answer = String::new();
        std::io::stdin().read_line(&mut answer).expect("Failed to read line.");
        let answer = answer.trim();

        match answer {
            "0" => break,
            "1" => {
                let distro = std::fs::read_to_string("/etc/os-release").expect("Failed to read os-release file.");
                if distro.contains("Arch") {
                    Command::new("clear").status().expect("Failed to clear screen.");
                    Command::new("topgrade").status().expect("Failed to run topgrade.");
                } else if distro.contains("Ubuntu") || distro.contains("Debian") {
                    Command::new("sudo")
                        .arg("apt")
                        .arg("update")
                        .status()
                        .expect("Failed to update with apt.");
                    Command::new("sudo")
                        .arg("apt")
                        .arg("upgrade")
                        .status()
                        .expect("Failed to upgrade with apt.");
                } else if distro.contains("Fedora") {
                    Command::new("sudo")
                        .arg("dnf")
                        .arg("update")
                        .status()
                        .expect("Failed to update with dnf.");
                } else {
                    println!("Distribution not supported for updating.");
                }
            }
            "2" => {
                let distro = std::fs::read_to_string("/etc/os-release").expect("Failed to read os-release file.");
                let package_manager = if distro.contains("Arch") {
                    "yay"
                } else if distro.contains("Ubuntu") {
                    "apt"
                } else if distro.contains("Fedora") {
                    "dnf"
                } else if distro.contains("Debian") {
                    "apt"
                } else {
                    panic!("Unsupported distribution.");
                };

                let package_file = match package_manager {
                    "yay" => "core-packages-arch.txt",
                    "apt" => {
                        if distro.contains("Debian") {
                            "core-packages-debian.txt"
                        } else {
                            "core-packages-ubuntu.txt"
                        }
                    },
                    "dnf" => "core-packages-fedora.txt",
                    _ => panic!("Unsupported package manager."),
                };

                Command::new("clear").status().expect("Failed to clear screen.");
                Command::new("wget")
                    .args(&["-O", package_file, &format!("https://raw.githubusercontent.com/SteavenToolBox/Arch/main/{}", package_file)])
                    .status()
                    .expect("Failed to download core packages file.");

                match package_manager {
                    "yay" => {
                        Command::new("sh")
                            .arg("-c")
                            .arg(format!("{} -Syu --noconfirm --needed < {}", package_manager, package_file))
                            .status()
                            .expect("Failed to install core packages.");
                    }
                    "apt" => {
                        Command::new("sudo")
                            .arg(package_manager)
                            .args(&["install", "-y", &format!("$(cat {})", package_file)])
                            .status()
                            .expect("Failed to install core packages.");
                    }
                    "dnf" => {
                        Command::new("sudo")
                            .arg(package_manager)
                            .args(&["install", "-y", &format!("$(cat {})", package_file)])
                            .status()
                            .expect("Failed to install core packages.");
                    }
                    _ => panic!("Unsupported package manager."),
                };
            }
            "3" => {
                Command::new("wget")
                    .args(&["-O", "gnome-packages.txt", "https://raw.githubusercontent.com/SteavenToolBox/Arch/main/gnome-packages.txt"])
                    .status()
                    .expect("Failed to download gnome-packages.txt.");
                Command::new("yay")
                    .args(&["-Syu", "--noconfirm", "--needed", "$(cat gnome-packages.txt)"])
                    .status()
                    .expect("Failed to install Gnome packages.");
            }
            "4" => {
                Command::new("wget")
                    .args(&["-O", "kde-packages.txt", "https://raw.githubusercontent.com/SteavenToolBox/Arch/main/kde-packages.txt"])
                    .status()
                    .expect("Failed to download kde-packages.txt.");
                Command::new("yay")
                    .args(&["-Syu", "--noconfirm", "--needed", "$(cat kde-packages.txt)"])
                    .status()
                    .expect("Failed to install KDE packages.");
            }
            "5" => {
                Command::new("wget")
                    .args(&["-O", "i3-packages.txt", "https://raw.githubusercontent.com/SteavenToolBox/Arch/main/i3-packages.txt"])
                    .status()
                    .expect("Failed to download i3-packages.txt.");
                Command::new("yay")
                    .args(&["-Syu", "--noconfirm", "--needed", "$(cat i3-packages.txt)"])
                    .status()
                    .expect("Failed to install i3 packages.");
            }
            "6" => {
                Command::new("wget")
                    .args(&["-O", "hyprland-packages.txt", "https://raw.githubusercontent.com/SteavenToolBox/Arch/main/hyprland-packages.txt"])
                    .status()
                    .expect("Failed to download hyprland-packages.txt.");
                Command::new("yay")
                    .args(&["-Syu", "--noconfirm", "--needed", "$(cat hyprland-packages.txt)"])
                    .status()
                    .expect("Failed to install Hyprland packages.");
            }
            "7" => {
                Command::new("yay")
                    .args(&["-Syu", "--noconfirm", "--needed", "aur/lib32-nvidia-utils-beta", "aur/lib32-opencl-nvidia-beta", "aur/nvidia-beta-dkms", "aur/nvidia-settings-beta", "aur/nvidia-utils-beta", "aur/opencl-nvidia-beta"])
                    .status()
                    .expect("Failed to install Nvidia Beta Drivers.");
                Command::new("sudo")
                    .args(&["systemctl", "enable", "nvidia-suspend.service"])
                    .status()
                    .expect("Failed to enable nvidia-suspend service.");
                Command::new("sudo")
                    .args(&["systemctl", "enable", "nvidia-resume.service"])
                    .status()
                    .expect("Failed to enable nvidia-resume service.");
                Command::new("sudo")
                    .args(&["systemctl", "enable", "nvidia-hibernate.service"])
                    .status()
                    .expect("Failed to enable nvidia-hibernate service.");
            }
            "8" => {
                Command::new("git")
                    .args(&["clone", "https://github.com/SteavenGamerYT/SteavenSettings"])
                    .status()
                    .expect("Failed to clone SteavenSettings repository.");
                Command::new("cd")
                    .arg("SteavenSettings")
                    .status()
                    .expect("Failed to change directory to SteavenSettings.");
                Command::new("./install.sh")
                    .status()
                    .expect("Failed to run install.sh.");
            }
            _ => {
                println!("Quitting...");
                run = 0; // set run flag to 0 so program will end
            }
        }
    }
}

