import gnupg
import hashlib
import tomllib
import os
import subprocess
import shutil
from cli import REGISTRY_BASE

def opengpg_check(name: str, author: str) -> bool:
    gpg = gnupg.GPG()
    package_dir = f"{REGISTRY_BASE}/{author}"
    toml_path = f"{package_dir}/{name}.toml"

    try:
        with open(toml_path, "rb") as f:
            meta = tomllib.load(f)
    except Exception:
        return False

    security = meta.get("security", {})
    key_file = security.get("opengpg")
    expected_hash = security.get("sha256")
    
    target_file = f"{package_dir}/{name}.tar.gz"
    key_path = f"{package_dir}/{key_file}"
    sig_path = f"{target_file}.asc"

    if not os.path.exists(target_file):
        return False

    sha256_hash = hashlib.sha256()
    with open(target_file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    if sha256_hash.hexdigest() != expected_hash:
        return False

    if not os.path.exists(key_path) or not os.path.exists(sig_path):
        return False

    with open(key_path, "r") as f:
        gpg.import_keys(f.read())

    with open(target_file, "rb") as f:
        verified = gpg.verify_file(f, sig_file=sig_path)

    if verified.status == "signature good" or verified.valid:
        return True
    
    return False

def run_sandboxed_build(name: str, author: str, stage_dir: str) -> bool:
    package_dir = f"{REGISTRY_BASE}/{author}"
    toml_path = f"{package_dir}/{name}.toml"

    try:
        with open(toml_path, "rb") as f:
            meta = tomllib.load(f)
    except Exception:
        return False

    build_cfg = meta.get("build", {})
    cores = os.cpu_count() or 1
    
    if os.path.exists(stage_dir):
        shutil.rmtree(stage_dir)
    os.makedirs(stage_dir)

    env = {
        "PATH": "/usr/bin:/bin:/usr/local/bin",
        "DESTDIR": stage_dir,
        "HOME": "/tmp"
    }

    cmds = [
        build_cfg.get("configure"),
        build_cfg.get("compile", "").format(cores=cores),
        build_cfg.get("install", "").format(stagedir=stage_dir)
    ]

    os.chdir(package_dir)

    for cmd in cmds:
        if not cmd: continue
        try:
            subprocess.run(
                ["unshare", "-n", "sh", "-c", cmd],
                env=env,
                check=True
            )
        except subprocess.CalledProcessError:
            return False

    return True

if __name__ == "__main__":
    print("This module is a component of the package manager and should not be run directly.")