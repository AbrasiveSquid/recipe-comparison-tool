import os

class Config:
    SECRET_KEY = os.environ.get("Secret_Key")

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable is required")
