import os
import asyncio
import aiohttp
import logging
from typing import Optional
from asyncio import Queue

from .predicate import Predicate
from .exceptions import RemotePredicateFetchError

logger = logging.getLogger(__name__)

class RemotePredicateResource:
    def __init__(self, url: str) -> None:
        self._url = url.rstrip("/") + "/api/v1/predicate"
        self._etag: Optional[str] = None
        self._predicate: Optional[Predicate] = None
        self._lock = asyncio.Lock()
        self._loaded_once_future = asyncio.get_event_loop().create_future()
        self._predicate_queue: Queue[Predicate] = Queue()

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

    def get_update_queue(self) -> Queue:
        return self._predicate_queue

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
                    if self._predicate and self._predicate.to_dict() == new_predicate.to_dict():
                        return
                    self._predicate = new_predicate
                    await self._predicate_queue.put(new_predicate)

                    if not self._loaded_once_future.done():
                        self._loaded_once_future.set_result(True)
