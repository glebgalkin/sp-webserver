from pathlib import Path
import mimetypes
import random

FILES_DIR = Path.cwd() / 'files'
CONTENT_TYPE_TO_EXTENSION = {
    "text/plain": ".txt",
    "text/html": ".html",
    "text/css": ".css",
    "text/javascript": ".js",
    "application/json": ".json",
    "application/xml": ".xml",
    "application/pdf": ".pdf",
    "application/zip": ".zip",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "video/mp4": ".mp4",
    "video/webm": ".webm",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.ms-powerpoint": ".ppt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
}


def get_file(filename: str) -> Path | None:
    file_path = FILES_DIR / filename
    return file_path if file_path.is_file() else None

def get_content_type(filename: str) -> str:
    content_type, _ = mimetypes.guess_type(filename)
    return content_type or 'application/octet-stream'

def get_file_extension(header_content_type: str) -> str:
    content_type = header_content_type.strip()
    if not content_type:
        raise ValueError("None header_content_type provided to get_file_extension()")
    if content_type not in CONTENT_TYPE_TO_EXTENSION:
        return '.bin'
    return CONTENT_TYPE_TO_EXTENSION[content_type]

def get_file_size_bytes(filepath: Path) -> int:
    return filepath.stat().st_size

def save_file(file: bytes, content_type: str):
    filename = get_random_filename() + get_file_extension(content_type)
    file_path = FILES_DIR / filename
    with open(file_path, 'wb') as f:
        f.write(file)

def get_random_filename() -> str:
    random_int = random.randint(1, 20)
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random_int)])
