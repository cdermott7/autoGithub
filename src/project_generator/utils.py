import re

def sanitize_filename(filename):
    # Remove invalid characters and replace spaces with underscores
    sanitized = re.sub(r'[^\w\-_\. ]', '', filename)
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized.lower()
