import os
import sys

# Ensure root directory is on python path for Vercel serverless functions
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app as flask_app

class VercelWSGIHandler:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "/")
        if path.startswith("/api/index.py"):
            environ["PATH_INFO"] = path[13:] or "/"
        elif path.startswith("/api/index"):
            environ["PATH_INFO"] = path[10:] or "/"
        return self.app(environ, start_response)

# Export app handler for Vercel
app = VercelWSGIHandler(flask_app)

