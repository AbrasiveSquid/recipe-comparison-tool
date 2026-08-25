import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable is required")
