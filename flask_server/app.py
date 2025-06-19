from flask import Flask
import logging
import sys

from predicate_updater import start_updater
from routes.predicate_route import register_routes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

register_routes(app)

start_updater()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
