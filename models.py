# models.py
# Shared message models for agent-to-agent communication

from uagents import Model

class PriceRequest(Model):
    token: str
    current_price: float
    entry_price: float
    historical_prices: list
    current_holdings: float

class TradeSignal(Model):
    signal: str
    percent: float

class PriceResponse(Model):
    token: str
    price: float
    timestamp: str