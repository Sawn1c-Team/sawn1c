import sys
import requests
import tomllib
import zipfile
import io

REGISTRY_BASE = "https://raw.githubusercontent.com/sawn1c-repos/registry/main/packages"

def install(name):
    # 1. Pull the .toml
    url = f"{REGISTRY_BASE}/{name}.toml"
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
