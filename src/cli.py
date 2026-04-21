import subprocess
import requests
import tomllib
import zipfile
import io
from . import security


REGISTRY_BASE = "https://raw.githubusercontent.com/sawn1c-repos/registry/main/packages"


def error(msg: str) -> None:
    print(f"Error: {msg}")


def install(name, author):
    # 1. Pull the .toml
    url = f"{REGISTRY_BASE}/{author}/{name}.toml"
    if not security.opengpg_check(name=name, author=author):
        print("Package check failed, This means the SHA256 or OpenGPG check failed")
    else:
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Package '{name}' not found.")
            return

        # 2. Parse it
        meta = tomllib.loads(res.text)
        download_url = meta["package"]["download"]
        print(f"Installing {meta['package']['name']} v{meta['package']['version']}...")

        # 3. Download and extract
        data = requests.get(download_url).content
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            z.extractall(f"./installed/{name}")

        print("Done.")
        subprocess.run(["touch", "installedpkgs.toml"])
        with open("installedpkgs.toml", "a") as f:
            f.write(f'{name} = "{meta["package"]["version"]}"\n')


def uninstall(name, author):
    # 1. Pull the .toml
    url = f"{REGISTRY_BASE}/{author}/{name}.toml"
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Package '{name}' not found.")
        return

    # 2. Parse it
    meta = tomllib.loads(res.text)  # noqa: F841

    # 3. Remove the package
    subprocess.run(["rm", "-rf", f"./installed/{name}"])

    # 4. Remove from installedpkgs.toml
    with open("installedpkgs.toml", "r") as f:
        lines = f.readlines()
    with open("installedpkgs.toml", "w") as f:
        for line in lines:
            if not line.startswith(f"{name} ="):
                f.write(line)

    print("Done.")
