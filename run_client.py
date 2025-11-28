# run_client.py
from agent_client import AgentClient
import threading, time, asyncio

client = AgentClient(client_name="my-app-user-1", client_port=8003)

# Start the client's agent in a background thread (this starts its server/context)
threading.Thread(target=client.run, daemon=True).start()
time.sleep(1)  # give it a moment to initialize

async def main():
    query = "I bought 3 SOL at $20, i want to sell and buy Ethereum (ETH) is that a good move?"
    response = await client.send_query(query, timeout=30)
    if response:
        print("\n📊 Agent Response:\n", response)
    else:
        print("No response received (timeout or other issue)")

asyncio.run(main())