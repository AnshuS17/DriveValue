import os
import sys

# Ensure root directory is on python path for Vercel serverless functions
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app

# Export application for Vercel Serverless Function
app = app


