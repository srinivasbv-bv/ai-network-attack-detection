import os
import sys

os.environ["VERCEL"] = "1"

# Add root directory to sys.path for Vercel Serverless environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from web.app import app

# Vercel WSGI Handler
app = app
