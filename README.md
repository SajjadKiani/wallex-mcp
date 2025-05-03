# Wallex MCP Server

## structure

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
│
├── examples/
│   └── wallex_demo.py     # Sample client invoking your MCP server
│
├── tests/
│   ├── test_client.py
│   ├── test_tools.py
│   └── test_resources.py
│
├── pyproject.toml
├── justfile              # Common dev tasks (lint, test, run)
├── Dockerfile
└── README.md             # Project overview + Quickstart

## Workflow

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
