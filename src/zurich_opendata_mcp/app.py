"""Shared FastMCP instance.

Lives in its own module so tool/resource modules can import it without
creating a cycle through ``server.py``.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

# FastMCP auto-enables DNS-rebinding protection (allowed hosts: localhost only)
# whenever it is constructed with the default 127.0.0.1 host, before server.py
# rebinds to `::` for Railway's IPv6 private network. That rejects the
# `*.railway.internal` Host header with HTTP 421. This is a private, read-only,
# no-auth service reached only over the private network, so the protection adds
# nothing here — disable it explicitly so any Host header is accepted.
mcp = FastMCP(
    "zurich_opendata_mcp",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    ),
)
