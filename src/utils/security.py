import hashlib
import secrets
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

def generate_api_key():
    return secrets.token_urlsafe(32)

def hash_api_key(api_key):
    return hashlib.sha256(api_key.encode()).hexdigest()

API_KEY = os.getenv('API_KEY', generate_api_key())
API_KEY_HASH = hash_api_key(API_KEY)

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        provided_api_key = request.headers.get('X-API-Key')
        if not provided_api_key or hash_api_key(provided_api_key) != API_KEY_HASH:
            return jsonify({"error": "Invalid or missing API key"}), 403
        return f(*args, **kwargs)
    return decorated_function

def sanitize_input(input_string):
    # Remove any potentially dangerous characters or patterns
    sanitized = input_string.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return sanitized
