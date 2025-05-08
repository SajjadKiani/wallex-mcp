# Wallex MCP Server

## development

``` bash
fastmcp dev wallex_mcp/server.py
```

## production

``` bash
mcpo --port 8001 --api-key "wallex-local" -- fastmcp run wallex_mcp/server.py
```

## structure

```
wallex-mcp/
├── wallex_mcp/
│   ├── __init__.py
│   ├── server.py          # FastMCP instantiation & run()
│   ├── config.py          # Env var loader
│   ├── client.py          # HTTPX wrapper
│   ├── schemas.py         # Pydantic models
│   ├── tools/
│   │   ├── get_balance.py     # @mcp.tool()
│   │   ├── place_order.py
│   │   └── cancel_order.py
│   └── resources/
│       ├── market_data.py     # @mcp.resource("wallex://market/{symbol}")
│       ├── order_status.py    # @mcp.resource("wallex://orders/{id}")
│       └── instruments.py
├── requirements.txt
├── Dockerfile
└── README.md             # Project overview + Quickstart
```


## Workflow

```
flowchart LR
  subgraph MCP Server
    A[FastMCP Instance] --> B[Tool: place_order]
    A --> C[Resource: get_balance]
    A --> D[Resource: market_data]
  end

  B --> E[wallex_mcp.client] --> F[Wallex REST API]
  C --> E
  D --> E
  F --> G[JSON Response] --> H[wallex_mcp.schemas] --> B/C/D return
  B/C/D return --> A --> I[LLM]
```