# solana_rag.py

import re
from hyperon import MeTTa, E, S, ValueAtom

class SolanaPortfolioRAG:
    def __init__(self, metta_instance: MeTTa):
        self.metta = metta_instance

    def get_token_category(self, token):
        """Find the category of a Solana token."""
        token = token.strip('"').upper()
        query_str = f'!(match &self (token_category $category {token}) $category)'
        results = self.metta.run(query_str)
        print(f"Token category query: {query_str} -> {results}")
        return [str(r[0]) for r in results if r and len(r) > 0] if results else []

    def get_token_volatility(self, token):
        """Find volatility level of a token."""
        token = token.strip('"').upper()
        query_str = f'!(match &self (volatility {token} $volatility) $volatility)'
        results = self.metta.run(query_str)
        print(f"Volatility query: {query_str} -> {results}")
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []

    def get_market_cap_tier(self, token):
        """Find market cap tier of a token."""
        token = token.strip('"').upper()
        query_str = f'!(match &self (market_cap {token} $cap) $cap)'
        results = self.metta.run(query_str)
        print(f"Market cap query: {query_str} -> {results}")
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []

    def get_protocol_token(self, protocol):
        """Get token associated with a DeFi protocol."""
        protocol = protocol.strip('"').lower()
        query_str = f'!(match &self (protocol {protocol} $token) $token)'
        results = self.metta.run(query_str)
        print(f"Protocol query: {query_str} -> {results}")
        return [str(r[0]) for r in results if r and len(r) > 0] if results else []

    def get_trading_signal(self, condition):
        """Get trading signal for market condition."""
        condition = condition.strip('"').lower()
        query_str = f'!(match &self (signal_condition {condition} $signal) $signal)'
        results = self.metta.run(query_str)
        print(f"Trading signal query: {query_str} -> {results}")
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []

    def get_risk_allocation(self, risk_level):
        """Get portfolio allocation strategy for risk level."""
        risk_level = risk_level.strip('"').lower()
        query_str = f'!(match &self (risk_allocation {risk_level} $allocation) $allocation)'
        results = self.metta.run(query_str)
        print(f"Risk allocation query: {query_str} -> {results}")
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []

    def get_market_strategy(self, market_condition):
        """Get strategy for market conditions."""
        market_condition = market_condition.strip('"').lower()
        query_str = f'!(match &self (market_strategy {market_condition} $strategy) $strategy)'
        results = self.metta.run(query_str)
        print(f"Market strategy query: {query_str} -> {results}")
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []

    def get_metric_analysis(self, metric):
        """Get analysis for trading metrics."""
        metric = metric.strip('"').lower()
        query_str = f'!(match &self (metric_analysis {metric} $analysis) $analysis)'
        results = self.metta.run(query_str)
        print(f"Metric analysis query: {query_str} -> {results}")
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []

    def get_trading_mistake_warning(self, mistake):
        """Get warning about common trading mistakes."""
        mistake = mistake.strip('"').lower()
        query_str = f'!(match &self (trading_mistake {mistake} $warning) $warning)'
        results = self.metta.run(query_str)
        print(f"Trading mistake query: {query_str} -> {results}")
        return [r[0].get_object().value for r in results if r and len(r) > 0] if results else []

    def query_portfolio_faq(self, question):
        """Retrieve portfolio analysis FAQ answers."""
        query_str = f'!(match &self (portfolio_faq "{question}" $answer) $answer)'
        results = self.metta.run(query_str)
        print(f"Portfolio FAQ query: {query_str} -> {results}")
        return results[0][0].get_object().value if results and results[0] else None

    def calculate_portfolio_risk(self, holdings):
        """Calculate overall portfolio risk based on token holdings."""
        total_risk_score = 0
        total_value = sum(holdings.values())
        
        for token, value in holdings.items():
            weight = value / total_value
            volatility = self.get_token_volatility(token)
            if volatility:
                vol_level = volatility[0]
                risk_score = {"low": 1, "high": 2, "very_high": 3, "extreme": 4}.get(vol_level, 2)
                total_risk_score += weight * risk_score
        
        return total_risk_score

    def generate_trading_signal(self, token, current_price, entry_price, historical_prices, holdings_pct):
        """Generate trading signal based on token analysis and portfolio data."""
        # Calculate price metrics
        unrealized_pnl = ((current_price - entry_price) / entry_price) * 100
        avg_historical = sum(historical_prices) / len(historical_prices) if historical_prices else current_price
        price_vs_avg = ((current_price - avg_historical) / avg_historical) * 100
        
        # Get token characteristics
        volatility = self.get_token_volatility(token)
        market_cap = self.get_market_cap_tier(token)
        category = self.get_token_category(token)
        
        # Generate signal logic
        signal = "HOLD"
        percentage = 0
        
        # DCA when down and not overweight
        if unrealized_pnl < -10 and holdings_pct < 50:
            signal = "BUY"
            percentage = min(15, 50 - holdings_pct)
        # Take profits when up significantly
        elif unrealized_pnl > 15 and holdings_pct > 5:
            signal = "SELL" 
            percentage = min(25, holdings_pct - 5)
        # Buy when below historical average (for non-meme tokens)
        elif price_vs_avg < -5 and category and "meme" not in category:
            signal = "BUY"
            percentage = 10
        # Sell when above historical average
        elif price_vs_avg > 10:
            signal = "SELL"
            percentage = 15
            
        return {
            "signal": signal,
            "percent": percentage,
            "analysis": {
                "unrealized_pnl": round(unrealized_pnl, 2),
                "price_vs_historical_avg": round(price_vs_avg, 2),
                "volatility": volatility[0] if volatility else "unknown",
                "market_cap": market_cap[0] if market_cap else "unknown",
                "category": category[0] if category else "unknown"
            }
        }

    def add_knowledge(self, relation_type, subject, object_value):
        """Add new Solana knowledge dynamically."""
        if isinstance(object_value, str):
            object_value = ValueAtom(object_value)
        self.metta.space().add_atom(E(S(relation_type), S(subject), object_value))
        return f"Added {relation_type}: {subject} → {object_value}"