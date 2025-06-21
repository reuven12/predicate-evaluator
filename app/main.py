import asyncio
import json
import logging
from types import SimpleNamespace
from typing import List

from predicate.logging_config import configure_logging
from predicate.remote_predicate_resource import RemotePredicateResource

logger = logging.getLogger(__name__)
configure_logging()


def build_namespace_from_path(path: str, value: object) -> SimpleNamespace:
    parts: List[str] = path.strip('.').split('.')
    current = value
    for attr in reversed(parts):
        current = SimpleNamespace(**{attr: current})
    return current


async def main() -> None:
    logger.info("🔄 Initialising RemotePredicateResource …")
    resource = await RemotePredicateResource.from_env()
    queue = resource.get_update_queue()

    try:
        while True:
            predicate = await queue.get()

            predicate_dict = predicate.to_dict()
            logger.info("📜 Updated predicate:\n%s", json.dumps(predicate_dict, indent=2))

            feature_path = predicate.feature
            test_value = 20

            obj = build_namespace_from_path(feature_path, test_value)
            result = predicate.evaluate(obj)

            logger.info(f"🔍 Evaluated {feature_path} = {test_value} → ✅ {result}")

    except asyncio.CancelledError:
        pass
    finally:
        logger.info("⏹️  Shutting down gracefully.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Received KeyboardInterrupt — exiting.")
