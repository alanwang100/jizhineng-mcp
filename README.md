# JiZhiMCP (极智MCP)

> Cross-platform MCP adaptation gateway: host any HTTP API as a standard MCP service and auto-distribute it to mainstream Agent platforms (Doubao, Tongyi, Wenxin, Claude, etc.) with unified auth and usage dashboard.
>
> 把普通 HTTP API 一键托管为标准 MCP 服务，自动适配分发到豆包、通义、文心、Claude 等主流 Agent 平台，统一鉴权、统一用量看板。

## What is JiZhiMCP?

JiZhiMCP is a hosted MCP gateway that turns plain HTTP APIs into standard Model Context Protocol (MCP) tools. Connect once, and your API becomes callable from any MCP-compatible agent or client.

- **One gateway, many platforms** — expose one endpoint, get auto-adapted tools for Doubao, Tongyi, Wenxin, Claude and other mainstream agents.
- **Built-in common tools** — weather, currency exchange, unit conversion, IP location, time zones, Chinese holidays, todo management, web fetching, tech news, and more.
- **Bring your own API** — host your custom HTTP API as MCP tools from the console, with centralized API keys and call tracking.

## Quick Start

### 1. Get an API Key

1. Visit <https://xn--5kvtwv52d.com/console> (JiZhiMCP console) and register/login.
2. Create a personal access token in the **API-Key** page (starts with `jzk_`).

### 2. Add the MCP Server

Add this server configuration to your MCP client (Claude Desktop, Cursor, Coze, etc.):

```json
{
  "mcpServers": {
    "jizhineng-mcp": {
      "type": "streamableHttp",
      "url": "https://mcp.xn--5kvtwv52d.com/mcp/gateway",
      "headers": {
        "Authorization": "Bearer ${JIZHINENG_API_KEY}"
      },
      "timeout": 30000
    }
  }
}
```

### 3. Use It

Ask your agent:

- "查一下北京的天气" / "What's the weather in Beijing?"
- "查一下今天的人民币兑美元汇率"
- "查一下明年春节是几号"
- "帮我查一下这个网页的内容"

## Built-in Tools

| Tool | Purpose | Main params |
|---|---|---|
| `weather_query` | Real-time weather & forecast by city / lat-lng | city / latitude / longitude / days |
| `currency_convert` | Currency exchange conversion | amount / from / to |
| `unit_convert` | Unit conversion (length/weight/temp/area...) | value / from_unit / to_unit |
| `ip_locate` | IP geolocation & network info | ip |
| `time_now` | Current time in a timezone | timezone / city |
| `holiday_cn` | Chinese public holidays | year / month |
| `todo_manage` | Todo management | action / item / ... |
| `web_fetch` | Fetch web page content | url |

Plus marketplace templates: `world_time`, `ip_info`, `hacker_news_search`, `exchange_rate`.

> The gateway also exposes your custom hosted services; call `tools/list` after connecting to get the full, live tool list and schemas.

## Repository Layout

```
jizhineng-mcp/
├── connector-meta.json     # Product metadata (name, description, examples)
├── mcp.json                # MCP server declaration
├── token-schema.json       # API-Key configuration schema
├── icon.svg                # Product icon
└── skills/
    └── jizhineng-mcp/
        └── SKILL.md        # Connector skill guide
```

## License

[MIT](./LICENSE)

## Links

- Console: <https://xn--5kvtwv52d.com/console>
- Gateway: <https://mcp.xn--5kvtwv52d.com/mcp/gateway>
