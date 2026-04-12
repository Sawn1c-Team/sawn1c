import platform
import os

def get_arch():
    machine = platform.machine().lower()

    if machine in ["x86_64", "amd64"]:
        return "x86_64"
    elif machine in ["aarch64", "arm64"]:
        return "aarch64"
    elif machine.startswith("arm"):
        return "arm"
    elif machine in ["i386", "i686"]:
        return "i386"
    else:
        return "unknown"

def get_os():
    system = platform.system()

    if system == "Darwin":
        return "macos"

    if system == "Linux":
        # Read /etc/os-release ourselves, no extra libraries needed
        os_release = {}
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line:
                        key, value = line.split("=", 1)
                        os_release[key] = value.strip('"')
        except FileNotFoundError:
            return "linux"

        dist_id = os_release.get("ID", "").lower()
        dist_like = os_release.get("ID_LIKE", "").lower()

        if dist_id == "arch" or "arch" in dist_like:
            return "arch"
        elif dist_id in ["ubuntu", "debian", "linuxmint"] or "debian" in dist_like:
            return "ubuntu"
        elif dist_id in ["fedora", "rhel", "centos"] or "fedora" in dist_like or "rhel" in dist_like:
            return "fedora"
        else:
            return "linux"

    return "unknown"