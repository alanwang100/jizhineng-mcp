---
name: jizhineng-mcp
description: 极智MCP 网关连接器：通过统一 MCP 网关调用已托管的工具（HTTP API → MCP 适配）。一个地址聚合高频通用工具（天气/汇率/单位换算/IP定位/时区/节假日/待办/网页抓取/DNS/搜索等）、跨 Agent 结算账本（账户/原子转账/计量/存证）与用户自定义托管服务，统一鉴权与错误码。当任务涉及"查天气、查汇率、查节假日、单位换算、IP 定位、网页抓取、搜科技资讯"、"多 Agent 协作的任务结算/计量/存证审计"或"调用用户通过极智MCP 托管的自定义 HTTP API"时使用。
---

# 极智MCP 连接器使用说明

本连接器将极智MCP 云端网关（https://mcp.xn--5kvtwv52d.com/mcp/gateway）接入 WorkBuddy。网关内置高频通用工具、跨 Agent 结算账本，也暴露用户通过极智MCP 控制台托管的自定义服务（工具名 = 控制台配置的 `tool_name`）。

## 连接前准备

1. 访问 https://xn--5kvtwv52d.com/console 注册/登录极智MCP控制台
2. 在「API-Key」页面创建个人访问令牌（格式 `sk-` 开头）
3. 如需调用自定义托管服务：在「服务管理」中创建服务并确保状态为启用
4. 在 WorkBuddy 连接器中填入该 API-Key 完成连接（强烈建议携带，用于识别调用方与限流；不携带时按 IP 限流）

## 支持的通用工具（自有 12 个）

| 工具名 | 用途 | 主要参数 |
|---|---|---|
| `weather_query` | 按城市/经纬度查询实时天气与未来预报 | city / latitude / longitude / days |
| `currency_convert` | 货币汇率换算 | amount / from / to |
| `unit_convert` | 通用单位换算（长度/重量/温度/面积等） | value / from_unit / to_unit |
| `ip_locate` | 查询 IP 地址的地理位置与网络信息 | ip |
| `time_now` | 查询指定时区的当前时间 | timezone / city |
| `holiday_cn` | 查询中国法定节假日安排 | year / month |
| `todo_manage` | 待办事项管理 | action / item / ... |
| `web_fetch` | 抓取网页正文内容 | url |
| `dns_lookup` | 解析域名 DNS 记录（A/AAAA/CNAME/MX/TXT/NS） | domain / type |
| `github_search` | 搜索 GitHub 仓库与代码 | query |
| `stackoverflow_search` | 搜索 Stack Overflow 问答 | query |
| `timestamp_convert` | 时间戳与日期互转 | value / mode |

## 跨 Agent 结算账本（5 个）

用于多 Agent 协作场景下的任务结算、用量计量与存证审计，形成不可篡改的债权债务账本。

| 工具名 | 用途 | 主要参数 |
|---|---|---|
| `settlement.account` | 开立/查询结算账户（余额） | mode / account_id |
| `settlement.transfer` | 账户间原子转账 credits（幂等、防负余额、哈希链存证） | from_account / to_account / amount / idempotency_key |
| `settlement.ledger` | 查询账户余额与往来流水（对账） | account_id / limit |
| `audit.record` | 调用存证审计，返回不可篡改的 SHA-256 哈希 | actor / action / target / detail |
| `metering.record` | 记录/查询跨 Agent 用量计量（按 actor 聚合） | mode / actor / metric / units |

> `settlement.transfer` 建议携带 `idempotency_key`：网络重试时不会重复结算。转账为原子操作（付款方扣款与收款方到账要么同时成功要么同时失败），并写入前后相连的哈希链，可审计、防篡改。

## 支持的通用工具（集市模板 4 个）

| 工具名 | 用途 | 主要参数 |
|---|---|---|
| `world_time` | 查询指定时区的当前时间与日期 | timezone |
| `ip_info` | 查询指定 IP 的地理位置与网络信息 | ip |
| `hacker_news_search` | 搜索 Hacker News 最新科技资讯与讨论 | query / hitsPerPage |
| `exchange_rate` | 查询主要货币兑某基准货币的实时汇率 | base / symbols |

> 网关还暴露用户通过极智MCP 控制台托管的自定义服务；连接后调用 `tools/list` 可获取完整、实时的工具清单与参数 Schema。

## 调用示例

```json
{
  "method": "tools/call",
  "params": {
    "name": "weather_query",
    "arguments": {
      "city": "北京",
      "days": 3
    }
  }
}
```

```json
{
  "method": "tools/call",
  "params": {
    "name": "currency_convert",
    "arguments": {
      "amount": 100,
      "from": "USD",
      "to": "CNY"
    }
  }
}
```

```json
{
  "method": "tools/call",
  "params": {
    "name": "settlement.transfer",
    "arguments": {
      "from_account": "orchestrator",
      "to_account": "agent-a",
      "amount": 5,
      "reason": "task.complete",
      "idempotency_key": "settle-001"
    }
  }
}
```

每个工具的准确参数以 `tools/list` 返回的 `inputSchema` 为准。

## 错误码说明（统一 JSON-RPC 错误）

| 错误码 | 含义 | 处理建议 |
|---|---|---|
| -32001 | 参数无法标准化 / 参数错误 | 检查参数是否符合 Schema，不要重试 |
| -32002 | 上游/工具执行超时 | 可稍后重试 |
| -32003 | 上游/工具执行失败 | 可稍后重试 |
| -32004 | 工具熔断降级中 | 可重试，响应附 retry_after_s |
| -32005 | 工具不存在 | 不可重试；检查工具名或到控制台启用服务 |
| -32006 | 触发限频 | 可重试，稍后重试 |

## 注意事项

- 推荐携带 `Authorization: Bearer *** API-Key 即可自动附带
- 内置工具无需预先配置即可调用；自定义服务需在控制台创建并启用
- 上游超时默认 30 秒
- 额度/用量可在控制台查看
