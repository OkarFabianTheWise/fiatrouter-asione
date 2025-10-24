# test_coingecko_integration.py
"""
Simple test script to verify CoinGecko integration functionality
"""

import re
from agent import extract_token_from_query

def test_token_extraction():
    """Test the token extraction function"""
    test_queries = [
        "What is the price of Pepe?",
        "SOL price please",
        "Check Bitcoin current value",
        "How much is Ethereum worth?",
        "What is Solana trading at?",
        "PEPE token analysis",
        "BTC cost today",
        "Get Cardano price",
        "Show me Raydium value",
        "Avalanche worth checking",
        "Chainlink trading at what?"
    ]
    
    print("🧪 Testing token extraction from queries:")
    print("-" * 50)
    
    for query in test_queries:
        token = extract_token_from_query(query)
        print(f"Query: '{query}'")
        print(f"Extracted Token: {token}")
        print()

def test_price_parsing():
    """Test parsing CoinGecko price responses"""
    sample_responses = [
        "The current price of Pepe (PEPE) is $7.14e-06 USD, as of 2025-10-24 19:36:46 UTC",
        "The current price of Solana (SOL) is $162.45 USD, as of 2025-10-24 19:36:46 UTC",
        "The current price of Bitcoin (BTC) is $67890.12 USD, as of 2025-10-24 19:36:46 UTC"
    ]
    
    print("🧪 Testing price parsing from CoinGecko responses:")
    print("-" * 50)
    
    price_pattern = r"price of .* is \$?([\d.e\-+]+)"
    
    for response in sample_responses:
        price_match = re.search(price_pattern, response, re.IGNORECASE)
        if price_match:
            price_value = float(price_match.group(1))
            print(f"Response: '{response}'")
            print(f"Extracted Price: ${price_value:.8f}")
            print()
        else:
            print(f"❌ Could not parse price from: '{response}'")
            print()

if __name__ == "__main__":
    test_token_extraction()
    test_price_parsing()
    print("✅ All tests completed!")