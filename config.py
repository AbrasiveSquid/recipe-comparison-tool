import os

class Config:
    SECRET_KEY = os.environ.get("Secret_Key") or "this-is-a-really-secret-key"
