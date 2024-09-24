use std::process::Command;

fn main() {
    let mut run = 1; // run flag
    
    // Check if /steaventoolbox and /steaventoolbox/tmp directories can be read and written by the current user
    let _create_directories = Command::new("sh")
        .arg("-c")
        .arg("sudo mkdir -p /steaventoolbox/tmp && sudo chmod 777 -R /steaventoolbox && sudo rm -rf /steaventoolbox/tmp/*")
        .status()
        .expect("Failed to create directories, set permissions, and empty tmp directory.");
        
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

    // Check if git is installed or not
    let git_check = Command::new("sh")
        .arg("-c")
        .arg("command -v wget")
        .output()
        .expect("Failed to check if wget is installed.");

    if !git_check.stdout.is_empty() {
        println!("git is already installed.");
    } else {
        println!("git could not be found, installing it.");
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
                cmd.arg("pacman").arg("-Syu").arg("--noconfirm").arg("--needed").arg("git");
                cmd
            }
            "apt" => {
                let mut cmd = Command::new("sudo");
                cmd.arg("apt").arg("install").arg("-y").arg("git");
                cmd
            }
            "dnf" => {
                let mut cmd = Command::new("sudo");
                cmd.arg("dnf").arg("install").arg("-y").arg("git");
                cmd
            }
            _ => panic!("Unsupported package manager."),
        };

        install_command.status().expect("Failed to install git.");
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
                .arg("/steaventoolbox/tmp/yay-bin") // Cloning yay to specified directory
                .status()
                .expect("Failed to clone yay repository.");
            Command::new("sh")
                .arg("-c")
                .arg("cd steavento/steaventoolbox/tmp/yay-bin && makepkg -si --noconfirm") // Changing directory to cloned yay directory
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

    // Check if RPM Fusion is installed or not
    if distro.contains("Fedora") {
        // Check if RPM Fusion is installed or not
        let rpm_fusion_check = Command::new("sudo")
            .arg("sh")
            .arg("-c")
            .arg("dnf list installed rpmfusion-free-release rpmfusion-nonfree-release")
            .output()
            .expect("Failed to check if RPM Fusion is installed.");

        if !rpm_fusion_check.stdout.is_empty() {
            println!("RPM Fusion repositories are already installed.");
        } else {
            Command::new("sudo")
                .arg("sh")
                .arg("-c")
                .arg("dnf install -y https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm")
                .status()
                .expect("Failed to install RPM Fusion repositories on Fedora.");
        }
        let core_check = Command::new("sudo")
            .arg("sh")
            .arg("-c")
            .arg("dnf list installed @core")
            .output()
            .expect("Failed to check if @core is installed on Fedora.");

        if !core_check.stdout.is_empty() {
            Command::new("sudo")
                .arg("sh")
                .arg("-c")
                .arg("dnf update @core")
                .status()
                .expect("Failed to update @core on Fedora.");
        }
    } else {
        println!("RPM FUSION repositories is not supported on this distribution.");
    }
    // Check if i386 repos are enabled on Ubuntu or Debian
    if distro.contains("Ubuntu") || distro.contains("Debian") {
        let i386_check = Command::new("sh")
            .arg("-c")
            .arg("dpkg --print-foreign-architectures")
            .output()
            .expect("Failed to check if i386 architecture is enabled.");

        if !i386_check.stdout.contains(&b"i386"[0]) {
            Command::new("sh")
                .arg("-c")
                .arg("sudo dpkg --add-architecture i386")
                .status()
                .expect("Failed to add i386 architecture.");

            Command::new("sh")
                .arg("-c")
                .arg("sudo apt update")
                .status()
                .expect("Failed to update apt after adding i386 architecture.");
        } else {
            println!("i386 repositories is already enabled.");
        }
    } else {
        println!("i386 repositories enabler is not supported on this distribution.");
    }

    while run == 1 {
        println!("========================================================");
        println!("SteavenToolbox-For-Linux | We care about your pc! Linux!");
        println!("========================================================");
        println!("1. Update Linux");
        println!("2. Install i3");
        println!("3. Install Sway");
        println!("4. Install Games");
        println!("5. Install Apps");
        println!("6. Install Printer Drivers");
        println!("7. Install Gpu Drivers");
        println!("8. Install SteavenSettings Incloudes Settings that fixs nvidia drivers as well");
        println!("9. Deblot Linux");
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
                let script_file = if distro.contains("Arch") {
                    "i3.sh"
                } else if distro.contains("Ubuntu") || distro.contains("Debian") {
                    "i3.sh"
                } else if distro.contains("Fedora") {
                    "i3.sh"
                } else {
                panic!("Unsupported distribution.");
                };
                let url = format!("https://github.com/SteavenToolBox/Linux/raw/refs/heads/main/scripts/{}/{}", if distro.contains("Arch") { "arch" } else if distro.contains("Ubuntu") || distro.contains("Debian") { "debian" } else { "fedora" }, script_file);
                Command::new("clear").status().expect("Failed to clear screen.");
                Command::new("wget")
                    .args(&["-O", &format!("/steaventoolbox/tmp/{}", script_file), &url])
                    .status()
                    .expect("Failed to download i3 script file.");
                Command::new("bash")
                    .arg(&format!("/steaventoolbox/tmp/{}", script_file))
                    .status()
                    .expect("Failed to execute i3 script.");
                }
            "3" => {
                let distro = std::fs::read_to_string("/etc/os-release").expect("Failed to read os-release file.");
                let script_file = if distro.contains("Arch") {
                    "sway.sh"
                } else if distro.contains("Ubuntu") || distro.contains("Debian") {
                    "sway.sh"
                } else if distro.contains("Fedora") {
                    "sway.sh"
                } else {
                panic!("Unsupported distribution.");
                };
                let url = format!("https://github.com/SteavenToolBox/Linux/raw/refs/heads/main/scripts/{}/{}", if distro.contains("Arch") { "arch" } else if distro.contains("Ubuntu") || distro.contains("Debian") { "debian" } else { "fedora" }, script_file);
                Command::new("clear").status().expect("Failed to clear screen.");
                Command::new("wget")
                    .args(&["-O", &format!("/steaventoolbox/tmp/{}", script_file), &url])
                    .status()
                    .expect("Failed to download i3 script file.");
                Command::new("bash")
                    .arg(&format!("/steaventoolbox/tmp/{}", script_file))
                    .status()
                    .expect("Failed to execute i3 script.");
                }
                "4" => {
                    let distro = std::fs::read_to_string("/etc/os-release").expect("Failed to read os-release file.");
                    let script_file = if distro.contains("Arch") {
                        "games.sh"
                    } else if distro.contains("Ubuntu") || distro.contains("Debian") {
                        "games.sh"
                    } else if distro.contains("Fedora") {
                        "games.sh"
                    } else {
                    panic!("Unsupported distribution.");
                    };
                    let url = format!("https://github.com/SteavenToolBox/Linux/raw/refs/heads/main/scripts/{}/{}", if distro.contains("Arch") { "arch" } else if distro.contains("Ubuntu") || distro.contains("Debian") { "debian" } else { "fedora" }, script_file);
                    Command::new("clear").status().expect("Failed to clear screen.");
                    Command::new("wget")
                        .args(&["-O", &format!("/steaventoolbox/tmp/{}", script_file), &url])
                        .status()
                        .expect("Failed to download i3 script file.");
                    Command::new("bash")
                        .arg(&format!("/steaventoolbox/tmp/{}", script_file))
                        .status()
                        .expect("Failed to execute i3 script.");
                    }
            "5" => {
                let distro = std::fs::read_to_string("/etc/os-release").expect("Failed to read os-release file.");
                let script_file = if distro.contains("Arch") {
                    "apps.sh"
                } else if distro.contains("Ubuntu") || distro.contains("Debian") {
                    "apps.sh"
                } else if distro.contains("Fedora") {
                    "apps.sh"
                } else {
                panic!("Unsupported distribution.");
                };
                let url = format!("https://github.com/SteavenToolBox/Linux/raw/refs/heads/main/scripts/{}/{}", if distro.contains("Arch") { "arch" } else if distro.contains("Ubuntu") || distro.contains("Debian") { "debian" } else { "fedora" }, script_file);
                Command::new("clear").status().expect("Failed to clear screen.");
                Command::new("wget")
                    .args(&["-O", &format!("/steaventoolbox/tmp/{}", script_file), &url])
                    .status()
                    .expect("Failed to download i3 script file.");
                Command::new("bash")
                    .arg(&format!("/steaventoolbox/tmp/{}", script_file))
                    .status()
                    .expect("Failed to execute i3 script.");
                }
            "6" => {
                let distro = std::fs::read_to_string("/etc/os-release").expect("Failed to read os-release file.");
                let script_file = if distro.contains("Arch") {
                    "printer.sh"
                } else if distro.contains("Ubuntu") || distro.contains("Debian") {
                    "printer.sh"
                } else if distro.contains("Fedora") {
                    "printer.sh"
                } else {
                panic!("Unsupported distribution.");
                };
                let url = format!("https://github.com/SteavenToolBox/Linux/raw/refs/heads/main/scripts/{}/{}", if distro.contains("Arch") { "arch" } else if distro.contains("Ubuntu") || distro.contains("Debian") { "debian" } else { "fedora" }, script_file);
                Command::new("clear").status().expect("Failed to clear screen.");
                Command::new("wget")
                    .args(&["-O", &format!("/steaventoolbox/tmp/{}", script_file), &url])
                    .status()
                    .expect("Failed to download i3 script file.");
                Command::new("bash")
                    .arg(&format!("/steaventoolbox/tmp/{}", script_file))
                    .status()
                    .expect("Failed to execute i3 script.");
                }
            "7" => {
                let distro = std::fs::read_to_string("/etc/os-release").expect("Failed to read os-release file.");
                let script_file = if distro.contains("Arch") {
                    "drivers.sh"
                } else if distro.contains("Ubuntu") || distro.contains("Debian") {
                    "drivers.sh"
                } else if distro.contains("Fedora") {
                    "drivers.sh"
                } else {
                panic!("Unsupported distribution.");
                };
                let url = format!("https://github.com/SteavenToolBox/Linux/raw/refs/heads/main/scripts/{}/{}", if distro.contains("Arch") { "arch" } else if distro.contains("Ubuntu") || distro.contains("Debian") { "debian" } else { "fedora" }, script_file);
                Command::new("clear").status().expect("Failed to clear screen.");
                Command::new("wget")
                    .args(&["-O", &format!("/steaventoolbox/tmp/{}", script_file), &url])
                    .status()
                    .expect("Failed to download i3 script file.");
                Command::new("bash")
                    .arg(&format!("/steaventoolbox/tmp/{}", script_file))
                    .status()
                    .expect("Failed to execute i3 script.");
                }
            "8" => {
                Command::new("sh")
                    .arg("-c")
                    .arg("sudo git clone https://github.com/SteavenGamerYT/SteavenSettings /steaventoolbox/tmp/steavensettings")
                    .status()
                    .expect("Failed to clone SteavenSettings repository.");
                Command::new("sh")
                    .arg("-c")
                    .arg("cd /steaventoolbox/tmp/steavensettings && ./install.sh")
                    .status()
                    .expect("Failed to run install.sh from SteavenSettings repository.");
            }
            "9" => {
                if distro.contains("Fedora") {
                    Command::new("sh")
                        .arg("-c")
                        .arg("sudo sh -c 'wget -O /steavengameryt/tmp/fedora-deblot.txt https://raw.githubusercontent.com/SteavenToolBox/Linux/main/fedora-deblot.txt'")
                        .status()
                        .expect("Failed to download Fedora deblot file.");
                    Command::new("sh")
                        .arg("-c")
                        .arg("sudo dnf remove -y $(cat /steavengameryt/tmp/fedora-deblot.txt)")
                        .status()
                        .expect("Failed to remove packages on Fedora using deblot file.");
                } else if distro.contains("Debian") {
                    println!("Debian is not supported for deblotting.");
                } else if distro.contains("Arch") {
                    println!("Arch is not supported for deblotting.");
                } else if distro.contains("Ubuntu") {
                    Command::new("sh")
                        .arg("-c")
                        .arg("sudo sh -c 'wget -O /steavengameryt/tmp/ubuntu-deblot.txt https://raw.githubusercontent.com/SteavenToolBox/Linux/main/ubuntu-deblot.txt'")
                        .status()
                        .expect("Failed to download Ubuntu deblot file.");
                    Command::new("sh")
                        .arg("-c")
                        .arg("sudo apt purge -y $(cat /steavengameryt/tmp/ubuntu-deblot.txt)")
                        .status()
                        .expect("Failed to purge packages on Ubuntu using deblot file.");
                }
            }
            _ => {
                println!("Quitting...");
                run = 0; // set run flag to 0 so program will end
            }
        }
    }
}



