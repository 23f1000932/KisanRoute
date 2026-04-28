import os
import atexit
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from routes.advisory import advisory_bp
from routes.mandis import mandis_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(advisory_bp, url_prefix="/api")
app.register_blueprint(mandis_bp, url_prefix="/api")

# Start background scheduler (daily data fetch from data.gov.in)
from scheduler import init_scheduler
_scheduler = init_scheduler()
atexit.register(lambda: _scheduler.shutdown(wait=False))


@app.route("/")
def health():
    return {"status": "KisanRoute backend is running", "version": "1.0.0"}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
