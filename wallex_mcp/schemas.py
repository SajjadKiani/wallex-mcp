from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderRequest(BaseModel):
    symbol: str
    side: OrderSide
    quantity: Decimal
    price: Decimal
    type: Optional[str] = Field("limit", alias="type")
    client_order_id: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


class Balance(BaseModel):
    currency: str
    available: Decimal
    locked: Decimal


class BalanceResponse(BaseModel):
    account_id: str
    balances: List[Balance]


class Order(BaseModel):
    id: str
    symbol: str
    side: OrderSide
    price: Decimal
    quantity: Decimal
    status: str
    created_at: datetime


class OrderResponse(BaseModel):
    order: Order


class Instrument(BaseModel):
    symbol: str
    base_asset: str
    quote_asset: str
    min_qty: Decimal
    tick_size: Decimal


class InstrumentsResponse(BaseModel):
    instruments: List[Instrument]


class Ticker(BaseModel):
    symbol: str
    price_change_percent: Decimal
    last_price: Decimal
    bid_price: Decimal
    ask_price: Decimal


class MarketDataResponse(BaseModel):
    ticker: Ticker
