# wallex_mcp/schemas.py
from decimal import Decimal
from typing import Dict, Optional, List
from pydantic import BaseModel, AliasChoices, Field, ConfigDict
from datetime import datetime
from enum import Enum

def camel_alias(field_name: str) -> str:
    """snake_case → camelCase for Wallex fields"""
    parts = field_name.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


class _WallexModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=camel_alias,
        extra="allow",  # ignore occasional undocumented fields
    )


# ---------- Shared wrappers ----------

class SuccessResponse(_WallexModel):
    success: bool
    message: str
    result: Dict[str, "T"]  # filled in by GenericModel at runtime


# ---------- /v1/markets ----------

class MarketStats(BaseModel):
    ch_24h: Decimal = Field(alias="24h_ch")              # 24‑hour price change
    ch_7d: Decimal = Field(alias="7d_ch")                # 7‑day  price change
    volume_24h: Decimal = Field(alias="24h_volume")      # 24‑hour volume
    volume_7d: Decimal = Field(alias="7d_volume")        # 7‑day  volume
    quote_volume_24h: Decimal = Field(alias="24h_quoteVolume")
    high_price_24h: Decimal = Field(alias="24h_highPrice")
    low_price_24h:  Decimal = Field(alias="24h_lowPrice")
    bid_price:      Decimal = Field(alias="bidPrice")
    ask_price:      Decimal = Field(alias="askPrice")

    model_config = {
        "populate_by_name": True,
        "extra": "allow",
    }


class Market(_WallexModel):
    symbol: str
    base_asset: str
    base_asset_precision: int
    quote_asset: str
    quote_precision: int
    fa_name: str
    fa_base_asset: str
    fa_quote_asset: str
    step_size: int
    tick_size: int
    min_qty: Decimal
    min_notional: Decimal
    stats: MarketStats

class MarketsResult(_WallexModel):
    symbols: Dict[str, Dict]

class MarketsResponse(SuccessResponse):
    symbols: Dict[str, Dict]


# ---------- /v1/account/assets ----------

class BalanceItem(_WallexModel):
    asset: str
    fa_name: str = Field(alias="faName")
    fiat: bool
    value: str
    locked: str
    asset_png_icon: str
    asset_svg_icon: str
    is_dust: bool
    is_digital_gold: bool

class BalancesResult(_WallexModel):
    balances: Dict[str, BalanceItem]

class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    OCO = "OCO"                  # One‑Cancels‑Other
    STOP_LIMIT = "STOP_LIMIT"
    STOP_MARKET = "STOP_MARKET"


class OrderStatus(str, Enum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"
    REJECTED = "REJECTED"


class Order(BaseModel):
    # ────────── core identifiers ──────────
    order_id: int = Field(alias="orderId")
    client_order_id: Optional[str] = Field(alias="clientOrderId", default=None)

    # ────────── instrument & side ─────────
    symbol: str
    side: OrderSide
    type: OrderType

    # ────────── requested amounts ─────────
    price: Decimal
    quantity_orig: Decimal = Field(alias="origQty")
    notional_orig: Decimal = Field(alias="origSum")     # = price × quantity

    # ────────── executed amounts ──────────
    price_exec: Optional[Decimal] = Field(alias="executedPrice", default=None)
    quantity_exec: Decimal = Field(alias="executedQty")
    notional_exec: Decimal = Field(alias="executedSum")
    percent_exec: Decimal = Field(alias="executedPercent")

    # ────────── state & flags ─────────────
    status: OrderStatus
    active: bool
    post_only: Optional[bool] = Field(default=None, alias="postOnly")
    reduce_only: Optional[bool] = Field(default=None, alias="reduceOnly")

    # ────────── timestamps ────────────────
    insert_time: Optional[datetime] = Field(alias="insertTime", default=None)
    update_time: Optional[datetime] = Field(alias="updateTime", default=None)

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )


class OrderResponse(SuccessResponse):
    result: Order

class OrderRequest(BaseModel):
    symbol: str
    type: OrderType
    side: OrderSide
    price: Decimal
    quantity: Decimal
    client_order_id: Optional[str] = Field(
        default=None, alias="clientOrderId",
        description="Optional user‑supplied ID (max 36 chars)."
    )

    # Wallex accepts camelCase, we expose snake_case
    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",          # catch typos early
    )


class OrdersResponse(SuccessResponse):
    result: List[Order]