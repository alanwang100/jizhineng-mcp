#!/usr/bin/env python3
"""
JiZhiMCP (极智MCP) quick-start example — no third-party dependencies.

Shows the full Model Context Protocol (MCP) over streamable-HTTP handshake:
  1. initialize  -> negotiate protocol version & capabilities
  2. tools/list  -> discover available tools
  3. tools/call  -> invoke one tool (e.g. weather_query)

Usage:
  python3 quickstart.py [GATEWAY_URL]
  python3 quickstart.py https://mcp.xn--5kvtwv52d.com/mcp/gateway

Set your API key (optional for anonymous rate-limited access):
  export JIZHINENG_API_KEY=sk-xxxx
"""

import json
import os
import sys
import urllib.request

DEFAULT_GATEWAY = "https://mcp.xn--5kvtwv52d.com/mcp/gateway"


def rpc(url: str, method: str, params: dict, api_key: str | None) -> dict:
    """Send a single JSON-RPC 2.0 message over streamable HTTP."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if api_key:
        headers["Authorization"] = "Bearer " + api_key

    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode()
        # streamable-http may return an SSE stream; take the JSON-RPC message.
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                line = line[5:].strip()
            if line.startswith("{"):
                return json.loads(line)
        return json.loads(body)


def main() -> None:
    gateway = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_GATEWAY
    api_key = os.environ.get("JIZHINENG_API_KEY")

    # 1. initialize
    init = rpc(
        gateway,
        "initialize",
        {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "jizhineng-quickstart", "version": "1.0.0"},
        },
        api_key,
    )
    server = init["result"]["serverInfo"]
    print("connected: %s v%s — %s" % (server["name"], server["version"], server["title"]))

    # 2. tools/list
    tools = rpc(gateway, "tools/list", {}, api_key)
    tool_list = tools["result"]["tools"]
    print("%d tools available:" % len(tool_list))
    for t in tool_list[:8]:
        print("   - %s: %s" % (t["name"], t.get("description", "")[:60]))

    # 3. tools/call — example: weather in Beijing
    print("\n-> calling weather_query for Beijing...")
    result = rpc(
        gateway,
        "tools/call",
        {"name": "weather_query", "arguments": {"city": "北京"}},
        api_key,
    )
    if "error" in result:
        print("error: %s" % result["error"])
    else:
        content = result["result"].get("content", [])
        text = content[0]["text"] if content else result["result"]
        print("result: %s" % text)


if __name__ == "__main__":
    main()
