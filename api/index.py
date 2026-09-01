import os
import sys

os.environ["VERCEL"] = "1"

# Add root directory to sys.path for Vercel Serverless environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from web.app import app
except Exception as e:
    import traceback
    err_str = traceback.format_exc()
    print(f"[Vercel Startup Error] {err_str}")
    from flask import Flask, jsonify
    app = Flask(__name__)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceback": err_str
        }), 500

# Vercel WSGI Handler
app = app
