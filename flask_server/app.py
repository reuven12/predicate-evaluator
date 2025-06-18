from flask import Flask, jsonify, request, make_response
import threading
import time
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

ETAG_VERSION = [1]
PREDICATE_JSON = [{
    "feature": ".x.y",
    "operation": {
        "operator": "and",
        "operations": [
            {"operator": "isNotNone"},
            {"operator": "isGreaterThan", "operand": 10}
        ]
    }
}]

@app.route("/api/v1/predicate")
def get_predicate():
    etag = f'"v{ETAG_VERSION[0]}"'
    if request.headers.get("If-None-Match") == etag:
        return "", 304
    response = make_response(jsonify(PREDICATE_JSON[0]))
    response.headers["ETag"] = etag
    return response

def update_predicate_loop():
    while True:
        time.sleep(120)
        ETAG_VERSION[0] += 1
        operand = 10 + ETAG_VERSION[0]
        PREDICATE_JSON[0] = {
            "feature": ".x.y",
            "operation": {
                "operator": "and",
                "operations": [
                    {"operator": "isNotNone"},
                    {"operator": "isGreaterThan", "operand": operand}
                ]
            }
        }
        logger.info(f"[Flask] Updated predicate to require y > {operand}, ETag: v{ETAG_VERSION[0]}")

threading.Thread(target=update_predicate_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
