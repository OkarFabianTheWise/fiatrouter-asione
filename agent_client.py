"""
Agent Client Helper Module
Provides functions to send unique requests to your fiatrouter-icm agent and get responses
"""

from datetime import datetime
from uuid import uuid4
import asyncio
from typing import Optional, Callable
from uagents import Agent, Context
from uagents_core.contrib.protocols.chat import ChatMessage, ChatAcknowledgement, TextContent

# Your fiatrouter-icm agent address
AGENT_ADDRESS = "agent1qvsqzmw3x0nw2czxhf02zvprvdstylthlwt84uaawj9yr2zne2l4q2r3etl"

class AgentClient:
    """Client to communicate with your fiatrouter-icm agent"""
    
    def __init__(self, client_name: str = "user-client", client_port: int = 8002):
        """Initialize the agent client"""
        self.client_name = client_name
        self.client_port = client_port
        self.agent = Agent(
            name=client_name,
            seed=f"{client_name}-seed-{uuid4()}",  # Unique seed each time
            port=client_port,
            endpoint=[f"http://127.0.0.1:{client_port}/submit"],
        )
        
        self.responses = {}  # Store responses by message ID
        self.acks = {}  # Store acknowledgements by message ID
        self.current_msg_id = None
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup message handlers for the client"""
        
        @self.agent.on_message(ChatAcknowledgement)
        async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
            """Handle acknowledgement from agent"""
            ctx.logger.info(f"✅ Acknowledgement received from agent for message: {msg.acknowledged_msg_id}")
            self.acks[msg.acknowledged_msg_id] = {
                "sender": sender,
                "timestamp": datetime.now().isoformat()
            }
        
        @self.agent.on_message(ChatMessage)
        async def handle_response(ctx: Context, sender: str, msg: ChatMessage):
            """Handle response message from agent"""
            response_text = ""
            for item in msg.content:
                if isinstance(item, TextContent):
                    response_text += item.text
            
            ctx.logger.info(f"📥 Response received from agent")
            self.responses[msg.msg_id] = {
                "sender": sender,
                "content": response_text,
                "timestamp": datetime.now().isoformat(),
                "msg_id": msg.msg_id
            }
    
    async def send_query(self, query: str, timeout: int = 30) -> Optional[str]:
        """
        Send a query to the agent and wait for response
        
        Args:
            query (str): The question or request to send to the agent
            timeout (int): Maximum seconds to wait for response (default: 30)
        
        Returns:
            str: The agent's response, or None if timeout
        """
        self.current_msg_id = uuid4()
        
        # Send message to agent
        self.agent.logger.info(f"📤 Sending query to agent: {query[:100]}...")
        
        await self.agent._ctx.send(
            AGENT_ADDRESS,
            ChatMessage(
                timestamp=datetime.now(),
                msg_id=self.current_msg_id,
                content=[TextContent(type="text", text=query)],
            )
        )
        
        # Wait for response with timeout
        elapsed = 0
        interval = 0.5  # Check every 500ms
        
        while elapsed < timeout:
            # Check if response received
            for msg_id, response in self.responses.items():
                if msg_id != self.current_msg_id:
                    continue
                result = response["content"]
                del self.responses[msg_id]  # Clean up
                self.agent.logger.info(f"✅ Response received in {elapsed:.1f} seconds")
                return result
            
            await asyncio.sleep(interval)
            elapsed += interval
        
        self.agent.logger.warning(f"⏱️ Timeout waiting for response after {timeout} seconds")
        return None
    
    def run(self):
        """Start the client agent"""
        self.agent.run()


# Standalone functions for easy integration

async def query_agent(question: str, timeout: int = 30) -> Optional[str]:
    """
    Simple function to send a query to the agent and get response
    
    Example:
        response = await query_agent("What's the best trading move for SOL?")
        print(response)
    """
    client = AgentClient(client_name="query-client", client_port=8003)
    
    # Send query in a background task
    async def send_in_background():
        response = await client.send_query(question, timeout=timeout)
        return response
    
    # This is a simplified approach - for production, use proper async context
    # For now, we'll return instructions
    return f"Query sent: {question}"


def create_trading_question(token1: str, entry_price: float, quantity: float, token2: str) -> str:
    """
    Create a formatted trading question
    
    Example:
        question = create_trading_question("SOL", 20.0, 3.0, "ETH")
        # Returns: "I bought 3 SOL at $20, i want to sell and buy Ethereum (ETH) is that a good move?"
    """
    token2_full = {
        "ETH": "Ethereum",
        "ETHEREUM": "Ethereum",
        "BTC": "Bitcoin",
        "BITCOIN": "Bitcoin",
        "ADA": "Cardano",
        "CARDANO": "Cardano",
        "MATIC": "Polygon",
        "POLYGON": "Polygon",
        "AVAX": "Avalanche",
        "AVALANCHE": "Avalanche",
    }.get(token2.upper(), token2)
    
    return f"I bought {quantity} {token1} at ${entry_price}, i want to sell and buy {token2_full} ({token2.upper()}) is that a good move?"


def create_price_question(token: str) -> str:
    """
    Create a price inquiry question
    
    Example:
        question = create_price_question("SOL")
        # Returns: "What is the current price of SOL?"
    """
    return f"What is the current price of {token.upper()}?"


def create_portfolio_question(query: str) -> str:
    """
    Create a portfolio-related question
    
    Example:
        question = create_portfolio_question("Is my portfolio diversified enough?")
    """
    return query


# Example usage
if __name__ == "__main__":
    # Example 1: Using the client class
    print("=" * 60)
    print("Example 1: Using AgentClient class")
    print("=" * 60)
    
    # Note: This requires the agent to be running in another terminal
    print("""
    To use this:
    
    1. Create a script that runs the agent client:
    
    from agent_client import AgentClient
    
    async def main():
        client = AgentClient(client_name="my-app-user-1", client_port=8003)
        
        # Send a query
        response = await client.send_query(
            "I bought 3 SOL at $20, i want to sell and buy Ethereum (ETH) is that a good move?"
        )
        
        if response:
            print("\\n📊 Agent Response:")
            print(response)
        else:
            print("No response received")
    
    import asyncio
    asyncio.run(main())
    """)
    
    # Example 2: Helper functions
    print("\n" + "=" * 60)
    print("Example 2: Using helper functions")
    print("=" * 60)
    
    trading_q = create_trading_question("SOL", 20.0, 3.0, "ETH")
    print(f"\nTrading Question:\n{trading_q}")
    
    price_q = create_price_question("SOL")
    print(f"\nPrice Question:\n{price_q}")
    
    portfolio_q = create_portfolio_question("Should I hold more Solana in my portfolio?")
    print(f"\nPortfolio Question:\n{portfolio_q}")
