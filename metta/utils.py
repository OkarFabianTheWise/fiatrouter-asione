# utils.py

import json
from openai import OpenAI
from .investment_rag import SolanaPortfolioRAG

class LLM:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.asi1.ai/v1"
        )

    def create_completion(self, prompt, max_tokens=200):
        completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="asi1-mini",
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content

def get_trading_intent_and_data(query, llm):
    """Use ASI:One API to classify trading query and extract relevant data."""
    prompt = (
        f"Given the Solana trading/portfolio query: '{query}'\n"
        "Classify the intent as one of: 'portfolio_analysis', 'token_analysis', 'trading_signal', 'risk_assessment', 'market_condition', 'protocol_info', 'mistake_warning', 'faq', or 'unknown'.\n"
        "Extract the most relevant data (e.g., SOL, RAY, portfolio, conservative, bull_market, raydium) from the query.\n"
        "Return *only* the result in JSON format like this, with no additional text:\n"
        "{\n"
        "  \"intent\": \"<classified_intent>\",\n"
        "  \"data\": \"<extracted_data>\"\n"
        "}"
    )
    response = llm.create_completion(prompt)
    try:
        result = json.loads(response)
        return result["intent"], result["data"]
    except json.JSONDecodeError:
        print(f"Error parsing ASI:One response: {response}")
        return "unknown", None

def generate_trading_knowledge(query, intent, data, llm):
    """Use ASI:One to generate trading knowledge for new data."""
    if intent == "token_analysis":
        prompt = (
            f"Query: '{query}'\n"
            f"The Solana token '{data}' is not in my knowledge base. Provide analysis of this token including category, risk level, and key characteristics.\n"
            "Return *only* the analysis, no additional text."
        )
    elif intent == "protocol_info":
        prompt = (
            f"Query: '{query}'\n"
            f"The DeFi protocol '{data}' is not in my knowledge base. Provide information about this protocol and its token.\n"
            "Return *only* the protocol information, no additional text."
        )
    elif intent == "market_condition":
        prompt = (
            f"Query: '{query}'\n"
            f"The market condition '{data}' has no strategy in my knowledge base. Suggest appropriate trading approaches.\n"
            "Return *only* the strategy, no additional text."
        )
    elif intent == "faq":
        prompt = (
            f"Query: '{query}'\n"
            "This is a new Solana portfolio question not in my knowledge base. Provide a helpful, concise answer.\n"
            "Return *only* the answer, no additional text."
        )
    else:
        return None
    return llm.create_completion(prompt)

def process_trading_data(price_data, rag: SolanaPortfolioRAG):
    """Process PriceRequest data and generate trading signal."""
    token = price_data.get("token", "SOL")
    current_price = price_data.get("current_price", 0)
    entry_price = price_data.get("entry_price", 0) 
    historical_prices = price_data.get("historical_prices", [])
    current_holdings = price_data.get("current_holdings", 0)
    
    # Generate trading signal using RAG
    signal_result = rag.generate_trading_signal(
        token, current_price, entry_price, historical_prices, current_holdings
    )
    
    return {
        "signal": signal_result["signal"],
        "percent": signal_result["percent"],
        "analysis": signal_result["analysis"]
    }

def process_chat_query(query, rag: SolanaPortfolioRAG, llm: LLM):
    """Process natural language queries about Solana portfolio analysis."""
    intent, data = get_trading_intent_and_data(query, llm)
    print(f"Trading Intent: {intent}, Data: {data}")
    prompt = ""

    if intent == "portfolio_analysis":
        risk_allocation = rag.get_risk_allocation("moderate")  # Default to moderate
        if risk_allocation:
            prompt = (
                f"Query: '{query}'\n"
                f"Recommended Portfolio Allocation: {', '.join(risk_allocation)}\n"
                "Provide comprehensive Solana portfolio analysis and recommendations."
            )
        else:
            prompt = f"Query: '{query}'\nProvide general Solana portfolio analysis guidance."

    elif intent == "token_analysis" and data:
        token_category = rag.get_token_category(data)
        volatility = rag.get_token_volatility(data)
        market_cap = rag.get_market_cap_tier(data)
        
        if token_category or volatility or market_cap:
            prompt = (
                f"Query: '{query}'\n"
                f"Token: {data}\n"
                f"Category: {', '.join(token_category) if token_category else 'Unknown'}\n"
                f"Volatility: {', '.join(volatility) if volatility else 'Unknown'}\n"
                f"Market Cap: {', '.join(market_cap) if market_cap else 'Unknown'}\n"
                "Provide detailed token analysis and trading recommendations."
            )
        else:
            new_analysis = generate_trading_knowledge(query, intent, data, llm)
            if new_analysis:
                rag.add_knowledge("token_category", data, "unknown")
                print(f"Knowledge graph updated - Added token: '{data}'")
            prompt = (
                f"Query: '{query}'\n"
                f"Token: {data}\n"
                f"Analysis: {new_analysis or 'Token not found in database'}\n"
                "Provide token analysis based on available information."
            )

    elif intent == "trading_signal" and data:
        trading_signals = rag.get_trading_signal(data)
        if trading_signals:
            prompt = (
                f"Query: '{query}'\n"
                f"Market Condition: {data}\n"
                f"Recommended Signal: {', '.join(trading_signals)}\n"
                "Explain the trading signal and reasoning."
            )
        else:
            prompt = f"Query: '{query}'\nProvide general trading signal analysis for {data}."

    elif intent == "risk_assessment" and data:
        risk_allocation = rag.get_risk_allocation(data)
        if risk_allocation:
            prompt = (
                f"Query: '{query}'\n"
                f"Risk Level: {data}\n"
                f"Recommended Allocation: {', '.join(risk_allocation)}\n"
                "Provide risk assessment and portfolio allocation guidance."
            )
        else:
            prompt = f"Query: '{query}'\nProvide risk assessment guidance for {data} risk profile."

    elif intent == "protocol_info" and data:
        protocol_token = rag.get_protocol_token(data)
        if protocol_token:
            prompt = (
                f"Query: '{query}'\n"
                f"Protocol: {data}\n"
                f"Associated Token: {', '.join(protocol_token)}\n"
                "Provide protocol information and investment analysis."
            )
        else:
            new_info = generate_trading_knowledge(query, intent, data, llm)
            if new_info:
                print(f"Knowledge graph updated - Added protocol info: '{data}'")
            prompt = (
                f"Query: '{query}'\n"
                f"Protocol: {data}\n"
                f"Information: {new_info or 'Protocol not found in database'}\n"
                "Provide protocol analysis based on available information."
            )

    elif intent == "mistake_warning" and data:
        warning = rag.get_trading_mistake_warning(data)
        if warning:
            prompt = (
                f"Query: '{query}'\n"
                f"Trading Mistake: {data}\n"
                f"Warning: {', '.join(warning)}\n"
                "Provide detailed explanation of this trading mistake and how to avoid it."
            )
        else:
            prompt = f"Query: '{query}'\nProvide guidance about avoiding the trading mistake: {data}."

    elif intent == "faq":
        faq_answer = rag.query_portfolio_faq(query)
        if faq_answer:
            prompt = (
                f"Query: '{query}'\n"
                f"Answer: {faq_answer}\n"
                "Provide comprehensive explanation with Solana-specific context."
            )
        else:
            new_answer = generate_trading_knowledge(query, intent, data, llm)
            if new_answer:
                rag.add_knowledge("portfolio_faq", query, new_answer)
                print(f"Knowledge graph updated - Added FAQ: '{query}'")
            prompt = (
                f"Query: '{query}'\n"
                f"Answer: {new_answer or 'Information not available'}\n"
                "Provide helpful Solana portfolio guidance."
            )
    
    if not prompt:
        prompt = f"Query: '{query}'\nProvide general Solana portfolio analysis guidance."

    prompt += "\nFormat response as professional Solana trading analysis. Include appropriate disclaimers about trading risks."
    response = llm.create_completion(prompt, max_tokens=300)
    
    return {
        "selected_question": query,
        "humanized_answer": response
    }