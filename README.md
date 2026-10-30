# JiZhiMCP (极智MCP)
<p align="center">
  <a href="https://github.com/alanwang100/jizhineng-mcp/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/alanwang100/jizhineng-mcp?style=social" /></a>
  <a href="https://github.com/alanwang100/jizhineng-mcp/blob/main/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
  <img alt="MCP" src="https://img.shields.io/badge/MCP-gateway-7b5cff" />
</p>


> Cross-platform MCP adaptation gateway: host any HTTP API as a standard MCP service and auto-distribute it to mainstream Agent platforms (Doubao, Tongyi, Wenxin, Claude, etc.) with unified auth and usage dashboard. Built-in tamper-evident cross-agent settlement ledger for multi-agent task accounting.
>
> 把普通 HTTP API 一键托管为标准 MCP 服务，自动适配分发到豆包、通义、文心、Claude 等主流 Agent 平台，统一鉴权、统一用量看板；内置不可篡改的跨 Agent 结算账本。

## What is JiZhiMCP?

JiZhiMCP is a hosted MCP gateway that turns plain HTTP APIs into standard Model Context Protocol (MCP) tools. Connect once, and your API becomes callable from any MCP-compatible agent or client.

- **One gateway, many platforms** — expose one endpoint, get auto-adapted tools for Doubao, Tongyi, Wenxin, Claude and other mainstream agents.
- **Built-in common tools** — weather, currency exchange, unit conversion, IP location, time zones, Chinese holidays, todo management, web fetching, DNS lookup, code search, and more.
- **Cross-agent settlement** — a built-in tamper-evident settlement ledger (accounts, atomic transfers, idempotency, hash-chain audit) so multiple agents can settle task credits with each other.
- **Bring your own API** — host your custom HTTP API as MCP tools from the console, with centralized API keys and call tracking.

## Quick Start

### 1. Get an API Key

1. Visit <https://xn--5kvtwv52d.com/console> (JiZhiMCP console) and register/login.
2. Create a personal access token in the **API-Key** page (starts with `sk-`).

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

### General-purpose tools

| Tool | Purpose | Main params |
|---|---|---|
| `weather_query` | Real-time weather & forecast | city / latitude / longitude / days |
| `currency_convert` | Currency exchange conversion | amount / from / to |
| `unit_convert` | Unit conversion (length/weight/temp...) | value / from / to |
| `holiday_cn` | Chinese public holidays | year / month |
| `time_now` | Current time in a timezone | timezone / city |
| `ip_locate` | IP geolocation & network info | ip |
| `dns_lookup` | DNS records (A/AAAA/CNAME/MX/TXT/NS) | domain / type |
| `github_search` | Search GitHub repos & code | query |
| `stackoverflow_search` | Search Stack Overflow Q&A | query |
| `timestamp_convert` | Timestamp ↔ date conversion | value / mode |
| `web_fetch` | Fetch web page content | url |
| `todo_manage` | Todo list management | action / item |

### Cross-agent settlement tools

| Tool | Purpose | Main params |
|---|---|---|
| `settlement.account` | Open or query a settlement account | mode / account_id |
| `settlement.transfer` | Atomic credit transfer between two agents (idempotent, hash-chained) | from_account / to_account / amount / idempotency_key |
| `settlement.ledger` | Query an account's balance & transaction history | account_id / limit |
| `audit.record` | Immutable audit trail (SHA-256 digest) | actor / action / target |
| `metering.record` | Usage metering & aggregation per agent | mode / actor / metric / units |

### Marketplace templates

| Tool | Purpose | Main params |
|---|---|---|
| `exchange_rate` | Real-time exchange rates | base / symbols |
| `hacker_news_search` | Search Hacker News | query |
| `ip_info` | IP info | ip |
| `world_time` | World clock / timezone | timezone |

> 21 tools total (17 first-party + 4 marketplace templates). The full live list with exact schemas is returned by `tools/list`. The gateway also exposes your custom hosted services.

## Cross-Agent Settlement

极智MCP 内置一个**不可篡改的跨 Agent 结算账本**，让多个 Agent 在协作任务中彼此结算 credits：

- **Accounts & balances** — every agent gets a `settlement.account` with a credits balance.
- **Atomic transfers** — `settlement.transfer` moves credits between any two accounts atomically (all-or-nothing), with `idempotency_key` so network retries never double-charge.
- **Tamper-evident hash chain** — every ledger entry carries a SHA-256 digest chained to the previous entry, making the whole ledger auditable and tamper-evident.
- **Usage metering & audit** — `metering.record` aggregates resource usage per agent; `audit.record` leaves an immutable proof of what was done and when.

This makes JiZhiMCP a **neutral settlement layer for multi-agent workflows** — when agents collaborate and need to account for "who did what and who owes whom", the gateway can settle it on their behalf.

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
- Docs: <https://xn--5kvtwv52d.com/docs>
- 中文教程 (Chinese tutorials): <https://xn--5kvtwv52d.com/tutorial.html> · <https://xn--5kvtwv52d.com/api-to-mcp.html> · <https://xn--5kvtwv52d.com/what-is-mcp.html>
