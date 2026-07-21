"""Shared FastMCP instance.

Lives in its own module so tool/resource modules can import it without
creating a cycle through ``server.py``.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from .http_client import close_client


@asynccontextmanager
async def _lifespan(_server: FastMCP) -> AsyncIterator[None]:
    """Close the shared HTTP client's connection pool on server shutdown."""
    try:
        yield
    finally:
        await close_client()


# FastMCP auto-enables DNS-rebinding protection (allowed hosts: localhost only)
# whenever it is constructed with the default 127.0.0.1 host, before server.py
# rebinds to `::` for Railway's IPv6 private network. That rejects the
# `*.railway.internal` Host header with HTTP 421. This is a private, read-only,
# no-auth service reached only over the private network, so the protection adds
# nothing here — disable it explicitly so any Host header is accepted.
mcp = FastMCP(
    "zurich_opendata_mcp",
    lifespan=_lifespan,
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)
