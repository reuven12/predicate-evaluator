import asyncio
import json
import logging
from types import SimpleNamespace
from typing import List, Optional

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

    last_predicate_dict: Optional[dict] = None

    try:
        while True:
            predicate = resource.predicate
            if predicate:
                current_predicate_dict = predicate.to_dict()

                if current_predicate_dict != last_predicate_dict:
                    logger.info("📜 Current predicate:\n%s", json.dumps(current_predicate_dict, indent=2))
                    last_predicate_dict = current_predicate_dict

                feature_path = predicate.feature
                test_value = 20

                obj = build_namespace_from_path(feature_path, test_value)
                result = predicate.evaluate(obj)

                logger.info(f"🔍 Evaluated {feature_path} = {test_value} → ✅ {result}")
            else:
                logger.warning("⏳ Predicate not yet loaded")

            await asyncio.sleep(30)

    except asyncio.CancelledError:
        pass
    finally:
        logger.info("⏹️  Shutting down gracefully.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Received KeyboardInterrupt — exiting.")
