import os
import asyncio
import aiohttp
import json
import logging
from typing import Optional

from .predicate import Predicate
from .exceptions import PredicateError, RemotePredicateFetchError

logger = logging.getLogger(__name__)

class RemotePredicateResource:
    def __init__(self, url: str) -> None:
        self._url = url.rstrip("/") + "/api/v1/predicate"
        self._etag: Optional[str] = None
        self._predicate: Optional[Predicate] = None
        self._lock = asyncio.Lock()
        self._loaded_once_future = asyncio.get_event_loop().create_future()

    @classmethod
    async def from_env(cls) -> "RemotePredicateResource":
        base_url = os.getenv("PREDICATE_SERVICE_URL")
        if not base_url:
            raise EnvironmentError("Missing PREDICATE_SERVICE_URL environment variable")

        resource = cls(base_url)
        asyncio.create_task(resource._update_loop())

        await resource._loaded_once_future
        return resource

    @property
    def predicate(self) -> Optional[Predicate]:
        return self._predicate

    async def _update_loop(self) -> None:
        while True:
            try:
                await self._fetch_predicate()
            except Exception as e:
                logger.warning(f"Failed to fetch predicate: {e}")
            await asyncio.sleep(120)

    async def _fetch_predicate(self) -> None:
        headers = {}
        if self._etag:
            headers["If-None-Match"] = self._etag

        async with aiohttp.ClientSession() as session:
            async with session.get(self._url, headers=headers) as response:
                if response.status == 304:
                    logger.debug("Predicate not modified (304).")
                    return

                if response.status != 200:
                    raise RemotePredicateFetchError(f"Status: {response.status}")

                text = await response.text()
                self._etag = response.headers.get("ETag")
                new_predicate = Predicate.from_json(text)

                async with self._lock:
                    self._predicate = new_predicate
                    if not self._loaded_once_future.done():
                        self._loaded_once_future.set_result(True)

                logger.info("Predicate fetched and updated successfully.")
