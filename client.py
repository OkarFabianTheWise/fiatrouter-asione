from datetime import datetime
from uuid import uuid4
from uagents import Agent, Context
from uagents_core.contrib.protocols.chat import ChatMessage, ChatAcknowledgement, TextContent

# Your fiatrouter-icm agent address (from the agent.py logs)
AGENT_ADDRESS = "agent1qvsqzmw3x0nw2czxhf02zvprvdstylthlwt84uaawj9yr2zne2l4q2r3etl"
AGENT_ENDPOINT = "https://dadd8da3c139.ngrok-free.app/submit"

client = Agent(
    name="test-client",
    seed="test-seed-123",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],
)

@client.on_event("startup")
async def send_message(ctx: Context):
    ctx.logger.info(f"Sending message to {AGENT_ADDRESS}")
    await ctx.send(
        AGENT_ADDRESS, 
        ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text="I bought 3 SOL at $20, i want to sell and buy Ethereum (ETH) is that a good move?")],
        )
    )

@client.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    print(f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}")

@client.on_message(ChatMessage)
async def handle_response(ctx: Context, sender: str, msg: ChatMessage):
    for item in msg.content:
        if isinstance(item, TextContent):
            print(f"Response from agent: {item.text}")

client.run()