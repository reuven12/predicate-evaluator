import os
import asyncio
import pytest
from unittest.mock import patch, AsyncMock
from predicate.remote_predicate_resource import RemotePredicateResource
from predicate.exceptions import RemotePredicateFetchError


@pytest.mark.asyncio
async def test_missing_env_variable():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(EnvironmentError):
            await RemotePredicateResource.from_env()


@pytest.mark.asyncio
async def test_successful_predicate_fetch(monkeypatch):
    fake_json = '{"feature": ".x.y", "operation": {"operator": "isNotNone"}}'

    class MockResponse:
        status = 200
        headers = {"ETag": "v1"}

        async def text(self):
            return fake_json

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

    class MockSession:
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def get(self, url, headers=None): return MockResponse()

    monkeypatch.setenv("PREDICATE_SERVICE_URL", "http://testserver")

    with patch("aiohttp.ClientSession", return_value=MockSession()):
        resource = await RemotePredicateResource.from_env()
        assert resource.predicate is not None
