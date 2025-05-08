from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum
from typing import Literal

class Balance(BaseModel):
    currency: str
    available: Decimal
    locked: Decimal


class BalanceResponse(BaseModel):
    balances: Dict

class OrderResult(BaseModel):
    symbol: str
    type: str
    side: str
    price: Decimal
    orig_qty: Decimal = Field(..., alias='origQty')
    orig_sum: Decimal = Field(..., alias='origSum')
    executed_price: Decimal = Field(..., alias='executedPrice')
    executed_qty: Decimal = Field(..., alias='executedQty')
    executed_sum: Decimal = Field(..., alias='executedSum')
    executed_percent: int = Field(..., alias='executedPercent')
    status: str
    active: bool
    client_order_id: str = Field(..., alias='clientOrderId')
    created_at: datetime = Field(..., alias='created_at')

    class Config:
        allow_population_by_field_name = True
        # let you construct with either the field names or the original aliases
        # e.g. OrderResult(orig_qty="0.001", origQty="0.001") both work

class OrderResponse(BaseModel):
    success: bool
    message: str
    result: OrderResult

class OrderRequest(BaseModel):
    symbol: str
    type: Literal["LIMIT", "MARKET"]   # tighten to your API’s allowed types
    side: Literal["BUY", "SELL"]
    price: float
    quantity: float

class Instrument(BaseModel):
    symbol: str
    base_asset: str
    quote_asset: str
    min_qty: Decimal
    tick_size: Decimal


class InstrumentsResponse(BaseModel):
    result: List[Instrument]
    message: str
    success: bool


class Ticker(BaseModel):
    symbol: str
    price_change_percent: Decimal
    last_price: Decimal
    bid_price: Decimal
    ask_price: Decimal


class MarketDataResponse(BaseModel):
    ticker: Ticker
