# Streamable-HTTP MCP server image — used for Railway / container deploys.
# Local stdio usage (Claude Desktop etc.) does not need this; see README.
FROM python:3.12-slim

WORKDIR /app

# Install the package (and its runtime deps) from the project metadata.
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir .

# Bind every interface so Railway's private network (IPv6) can reach it.
# `--host`/`--port` also honour $HOST/$PORT, which Railway injects at runtime.
ENV HOST=:: \
    PORT=8000 \
    ZURICH_OPENDATA_LOG_LEVEL=INFO

EXPOSE 8000

# MCP endpoint is served at /mcp (FastMCP streamable-http default).
CMD ["zurich-opendata-mcp", "--http"]
