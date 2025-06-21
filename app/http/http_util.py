def parse_filename(request_path: str) -> str:
    return request_path.split('/')[-1]