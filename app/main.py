import asyncio
import json
import logging
from types import SimpleNamespace

from predicate.logging_config import configure_logging
from predicate.remote_predicate_resource import RemotePredicateResource

logger = logging.getLogger(__name__)
configure_logging()

async def main() -> None:
    logger.info("🔄 Initialising RemotePredicateResource …")
    resource = await RemotePredicateResource.from_env()

    while True:
        predicate = resource.predicate
        if not predicate:
            logger.error("❌ Predicate failed to load")
            return
        
        obj = SimpleNamespace(x=SimpleNamespace(y=15))
        result = predicate.evaluate(obj)
        logger.info("📜 Current predicate:\n%s", json.dumps(predicate.to_dict(), indent=2))
        logger.info("🔍 Evaluated y=15  →  %s", result)

        await asyncio.sleep(120)

if __name__ == "__main__":
    asyncio.run(main())
