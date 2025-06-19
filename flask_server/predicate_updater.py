import threading
import time
import logging
from predicate_data import ETAG_VERSION, PREDICATE_JSON, OPERATORS, CONDITION_TYPES

logger = logging.getLogger(__name__)

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

def start_updater():
    threading.Thread(target=update_predicate_loop, daemon=True).start()
