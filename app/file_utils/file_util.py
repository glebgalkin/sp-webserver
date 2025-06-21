from pathlib import Path
import mimetypes
import random

FILES_DIR = Path.cwd() / 'files'

def get_file(filename: str) -> Path | None:
    file_path = FILES_DIR / filename
    return file_path if file_path.is_file() else None

def get_content_type(filename: str) -> str:
    content_type, _ = mimetypes.guess_type(filename)
    return content_type or 'application/octet-stream'

def get_file_size_bytes(filepath: Path) -> int:
    return filepath.stat().st_size

def save_file(filename: str, file: bytes):
    file_path = FILES_DIR / filename
    with open(file_path, 'wb') as f:
        f.write(file)

def get_random_filename() -> str:
    random_int = random.randint(1, 20)
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random_int)])
