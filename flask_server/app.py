from flask import Flask, jsonify, request, make_response
import threading
import time
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

ETAG_VERSION = [1]

OPERATORS = ["and", "or"]

CONDITION_TYPES = ["isGreaterThan", "isEqualTo", "isLessThan"]

PREDICATE_JSON = [{}]

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
        version = ETAG_VERSION[0]

        operand = 10 + version

        operator = OPERATORS[version % len(OPERATORS)]

        condition_type = CONDITION_TYPES[version % len(CONDITION_TYPES)]

        PREDICATE_JSON[0] = {
            "feature": ".x.y",
            "operation": {
                "operator": operator,
                "operations": [
                    {"operator": "isNotNone"},
                    {"operator": condition_type, "operand": operand}
                ]
            }
        }

        logger.info(
            f"[Flask] Updated predicate: ({operator}) + condition={condition_type}, operand={operand}, ETag=v{version}"
        )

threading.Thread(target=update_predicate_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
