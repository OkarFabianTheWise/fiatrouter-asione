from uagents import Agent, Context, Model

# --- Message models (must match ai_trader.py) ---
class PriceRequest(Model):
    token: str
    current_price: float
    entry_price: float
    historical_prices: list
    current_holdings: float

class TradeSignal(Model):
    signal: str
    percent: float


# --- Create your local client agent ---
client = Agent(
    name="local_client",
    seed="trial human moon alpha feed curve solid permit silver reason guess",
    port=8001,
    mailbox=True,
    publish_agent_details=True,
)

# --- Address of your ai_trader (local or remote) ---
# Replace this if running locally with ai_trader.py
TARGET = "agent1qt326c09ppqxrynrne6frwku7duquhe9vtklaa7qkg5q0vy4lsvvwe5k67x"


# --- Startup event: send PriceRequest ---
@client.on_event("startup")
async def send_request(ctx: Context):
    payload = PriceRequest(
        token="SOL",
        current_price=180.5,
        entry_price=150,
        historical_prices=[140, 150, 160, 170, 180],
        current_holdings=25,
    )

    await ctx.send(TARGET, payload)
    ctx.logger.info(f"📤 Sent PriceRequest to {TARGET}")


# --- Handle TradeSignal reply from trader ---
@client.on_message(model=TradeSignal)
async def handle_response(ctx: Context, sender: str, msg: TradeSignal):
    ctx.logger.info(f"💬 Reply from {sender}: {msg.signal} {msg.percent}%")
    print(f"💬 Reply from {sender}: {msg.signal} {msg.percent}%")


# --- Run ---
if __name__ == "__main__":
    client.run()
