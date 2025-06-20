from pathlib import Path
import os

def get_file(filename: str) -> Path | None:
    file_dir = Path.cwd() / 'files'
    file_path = file_dir / filename
    if file_path.is_file():
        return file_path
    return None

def get_content_type(filename: str) -> str:
    if filename.endswith('html'):
        return 'application/json'
    elif filename.endswith('xml'):
        return 'application/xml'
    elif filename.endswith('txt'):
        return 'text/plain'
    elif filename.endswith('html'):
        return 'text/html'
    else:
        return 'application/octet-stream'

def get_file_size_bytes(filepath: Path) -> int:
    return os.path.getsize(filepath)