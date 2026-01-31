from database.postgres import PostgresClient
from elasticsearch.client import get_es_client

from dataclasses import dataclass
from typing import Optional, Any
import asyncio
import inspect

from database.postgres import PostgresClient
from elasticsearch.client import get_es_client

@dataclass
class Clients:
    postgres: Optional[PostgresClient] = None
    es: Optional[Any] = None  # replace Any with your ES client type if available

clients = Clients()

async def _maybe_await(fn_result):
    if inspect.isawaitable(fn_result):
        return await fn_result
    return fn_result

async def init_clients(settings) -> Clients:
    """
    Create and attach clients to the shared `clients` instance.
    Call from app startup (awaitable).
    """
    # postgres client (example)
    clients.postgres = PostgresClient(dsn=settings.DB_DSN)
    if hasattr(clients.postgres, "connect"):
        await _maybe_await(clients.postgres.connect())

    # elasticsearch client factory
    clients.es = get_es_client(settings.ELASTIC_URL)
    if hasattr(clients.es, "connect"):
        await _maybe_await(clients.es.connect())

    return clients

async def close_clients() -> None:
    """
    Gracefully close clients. Call from app shutdown.
    """
    for client in (clients.es, clients.postgres):
        if client is None:
            continue
        if hasattr(client, "close"):
            res = client.close()
            await _maybe_await(res)