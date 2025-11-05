import json
import platform
import urllib.request
from pathlib import Path

METADATA_URL = "https://github.com/QudsLab/PQChub/raw/refs/heads/main/bins/binaries.json"
CACHE_DIR = Path("download_cache")

def detect_platform() -> (bool, str):
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        if "64" in machine or "amd64" in machine:
            return (True, "windows-x64")
        else:
            return (True, "windows-x86")
    elif system == "darwin":
        if "arm" in machine or "aarch64" in machine:
            return (True, "macos-arm64")
        else:
            return (True, "macos-x86_64")
    elif system == "linux":
        if "aarch64" in machine or "arm64" in machine:
            return (True, "linux-aarch64")
        else:
            return (True, "linux-x86_64")
    else:
        raise (False, f"Unsupported platform: {system} {machine}")
def download_file(url, dest_path) -> (bool, str):
    try:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, dest_path)
        return (True, "Download successful")
    except Exception as e:
        return (False, str(e))
def get_binary_path(metadata_url, cache_dir) -> (bool, bool, str):
    try:
        platform_status, platform_id = detect_platform()
        if platform_status:
            with urllib.request.urlopen(metadata_url) as response:
                metadata = json.loads(response.read().decode('utf-8'))
            if platform_id in metadata['binaries']:
                binary_info = metadata['binaries'][platform_id]
                binary_url = binary_info['url']
                binary_filename = binary_info['filename']
                cached_path = cache_dir / platform_id / binary_filename
                if cached_path.exists():
                    return (True, False, str(cached_path))
                else:
                    download_file(binary_url, cached_path)
                    return (True, True, str(cached_path))
    except Exception as e:
        return (False, False, str(e))
    return (False, False, "Unsupported platform")