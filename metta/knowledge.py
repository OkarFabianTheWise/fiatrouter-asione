# knowledge.py

from hyperon import MeTTa, E, S, ValueAtom

def initialize_solana_knowledge(metta: MeTTa):
    """Initialize the MeTTa knowledge graph with Solana ecosystem, tokens, and trading data."""
    
    # Solana Token Categories → Tokens
    metta.space().add_atom(E(S("token_category"), S("blue_chip"), S("SOL")))
    metta.space().add_atom(E(S("token_category"), S("blue_chip"), S("USDC")))
    metta.space().add_atom(E(S("token_category"), S("blue_chip"), S("USDT")))
    metta.space().add_atom(E(S("token_category"), S("defi"), S("RAY")))
    metta.space().add_atom(E(S("token_category"), S("defi"), S("SRM")))
    metta.space().add_atom(E(S("token_category"), S("defi"), S("ORCA")))
    metta.space().add_atom(E(S("token_category"), S("defi"), S("JUP")))
    metta.space().add_atom(E(S("token_category"), S("meme"), S("WIF")))
    metta.space().add_atom(E(S("token_category"), S("meme"), S("BONK")))
    metta.space().add_atom(E(S("token_category"), S("gaming"), S("ATLAS")))
    metta.space().add_atom(E(S("token_category"), S("gaming"), S("POLIS")))
    
    # Token → Market Cap Tier
    metta.space().add_atom(E(S("market_cap"), S("SOL"), ValueAtom("large_cap")))
    metta.space().add_atom(E(S("market_cap"), S("USDC"), ValueAtom("large_cap")))
    metta.space().add_atom(E(S("market_cap"), S("RAY"), ValueAtom("mid_cap")))
    metta.space().add_atom(E(S("market_cap"), S("ORCA"), ValueAtom("mid_cap")))
    metta.space().add_atom(E(S("market_cap"), S("JUP"), ValueAtom("mid_cap")))
    metta.space().add_atom(E(S("market_cap"), S("WIF"), ValueAtom("small_cap")))
    metta.space().add_atom(E(S("market_cap"), S("BONK"), ValueAtom("micro_cap")))
    
    # Token → Volatility Level
    metta.space().add_atom(E(S("volatility"), S("SOL"), ValueAtom("high")))
    metta.space().add_atom(E(S("volatility"), S("USDC"), ValueAtom("low")))
    metta.space().add_atom(E(S("volatility"), S("USDT"), ValueAtom("low")))
    metta.space().add_atom(E(S("volatility"), S("RAY"), ValueAtom("very_high")))
    metta.space().add_atom(E(S("volatility"), S("ORCA"), ValueAtom("very_high")))
    metta.space().add_atom(E(S("volatility"), S("JUP"), ValueAtom("very_high")))
    metta.space().add_atom(E(S("volatility"), S("WIF"), ValueAtom("extreme")))
    metta.space().add_atom(E(S("volatility"), S("BONK"), ValueAtom("extreme")))
    
    # DeFi Protocols → Tokens
    metta.space().add_atom(E(S("protocol"), S("raydium"), S("RAY")))
    metta.space().add_atom(E(S("protocol"), S("orca"), S("ORCA")))
    metta.space().add_atom(E(S("protocol"), S("jupiter"), S("JUP")))
    metta.space().add_atom(E(S("protocol"), S("serum"), S("SRM")))
    metta.space().add_atom(E(S("protocol"), S("marinade"), S("MNDE")))
    
    # Trading Signal Conditions → Recommendations
    metta.space().add_atom(E(S("signal_condition"), S("oversold"), ValueAtom("BUY")))
    metta.space().add_atom(E(S("signal_condition"), S("overbought"), ValueAtom("SELL")))
    metta.space().add_atom(E(S("signal_condition"), S("accumulation_zone"), ValueAtom("DCA")))
    metta.space().add_atom(E(S("signal_condition"), S("profit_taking"), ValueAtom("SELL")))
    metta.space().add_atom(E(S("signal_condition"), S("sideways"), ValueAtom("HOLD")))
    
    # Portfolio Risk Levels → Allocation Strategy
    metta.space().add_atom(E(S("risk_allocation"), S("conservative"), ValueAtom("70% SOL/USDC, 30% stablecoins")))
    metta.space().add_atom(E(S("risk_allocation"), S("moderate"), ValueAtom("50% SOL, 30% DeFi tokens, 20% stables")))
    metta.space().add_atom(E(S("risk_allocation"), S("aggressive"), ValueAtom("40% SOL, 40% DeFi, 15% memes, 5% stables")))
    
    # Market Conditions → Strategy
    metta.space().add_atom(E(S("market_strategy"), S("bull_market"), ValueAtom("accumulate growth tokens, reduce stables")))
    metta.space().add_atom(E(S("market_strategy"), S("bear_market"), ValueAtom("increase stables, DCA blue chips")))
    metta.space().add_atom(E(S("market_strategy"), S("sideways"), ValueAtom("range trade, collect yield")))
    
    # Token Metrics → Analysis
    metta.space().add_atom(E(S("metric_analysis"), S("high_volume"), ValueAtom("strong momentum signal")))
    metta.space().add_atom(E(S("metric_analysis"), S("low_volume"), ValueAtom("weak conviction, avoid")))
    metta.space().add_atom(E(S("metric_analysis"), S("rising_tvl"), ValueAtom("protocol growth, bullish")))
    metta.space().add_atom(E(S("metric_analysis"), S("falling_tvl"), ValueAtom("capital flight, bearish")))
    
    # Common Trading Mistakes → Warnings  
    metta.space().add_atom(E(S("trading_mistake"), S("ape_into_memes"), ValueAtom("limit meme allocation to 5-10% max")))
    metta.space().add_atom(E(S("trading_mistake"), S("fomo_buying"), ValueAtom("wait for retracements, use DCA")))
    metta.space().add_atom(E(S("trading_mistake"), S("panic_selling"), ValueAtom("stick to plan, zoom out timeframe")))
    metta.space().add_atom(E(S("trading_mistake"), S("overleverage"), ValueAtom("never risk more than you can lose")))
    
    # Portfolio Analysis FAQs
    metta.space().add_atom(E(S("portfolio_faq"), S("How to analyze Solana portfolio?"), ValueAtom("Check token allocation, risk distribution, and correlation")))
    metta.space().add_atom(E(S("portfolio_faq"), S("When to rebalance?"), ValueAtom("Monthly or when allocation drifts >10% from target")))
    metta.space().add_atom(E(S("portfolio_faq"), S("Best Solana DeFi tokens?"), ValueAtom("RAY, ORCA, JUP for established protocols")))
    metta.space().add_atom(E(S("portfolio_faq"), S("How much SOL to hold?"), ValueAtom("30-50% for most Solana portfolios")))