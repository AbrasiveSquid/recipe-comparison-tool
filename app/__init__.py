from flask import Flask, request
from flask_limiter import Limiter

from config import Config

def get_client_ip():
    forwarded_for = request.headers.get("X-Forwarded-For")

    if forwarded_for:
        return forwarded_for.rsplit(",", 1)[-1].strip()

    return request.remote_addr or "127.0.0.1"

app = Flask(__name__)
app.config.from_object(Config)

limiter = Limiter(
    key_func=get_client_ip,
    app=app,
    storage_uri="memory://",
)

from app import routes
