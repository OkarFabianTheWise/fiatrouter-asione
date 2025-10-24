# Solana Portfolio Analyzer Agent - Fetch.ai & MeTTa Integration

A demonstration of how to integrate **SingularityNET's MeTTa Knowledge Graph** with **Fetch.ai's uAgents** to create intelligent, autonomous agents that can analyze Solana portfolios and generate trading signals using structured DeFi knowledge reasoning.

## 🤖 What is MeTTa by SingularityNET?

**MeTTa** (Meta Type Talk) is a multi-paradigm language for declarative and functional computations over knowledge (meta)graphs developed by SingularityNET. It provides a powerful framework for:

- **Structured Knowledge Representation**: Organize information in logical, queryable formats
- **Symbolic Reasoning**: Perform complex logical operations and pattern matching
- **Knowledge Graph Operations**: Build, query, and manipulate knowledge graphs

MeTTa uses a space-based architecture where knowledge is stored as atoms in logical spaces, enabling sophisticated querying and reasoning capabilities.

## 🔗 What is Fetch.ai?

**Fetch.ai** provides a complete ecosystem for building, deploying and discovering AI Agents. Key features include:

- **uAgents Framework**: Python-based framework for building autonomous agents
- **Agentverse**: Open marketplace for agent discovery and interaction
- **Chat Protocol**: Standardized communication protocol to make agents discoverable through ASI:One
- **ASI:One**: An agentic LLM that can interact with different agents on Agentverse to answer user queries.

## 🧠 MeTTa Components Explained

### Core MeTTa Elements

#### 1. **Space (Knowledge Container)**

```python
metta = MeTTa()  # Creates a new MeTTa instance with a space
```

The space is where all knowledge atoms are stored and queried.

#### 2. **Atoms (Knowledge Units)**

Atoms are the fundamental units of knowledge in MeTTa:

- **E (Expression)**: Creates logical expressions
- **S (Symbol)**: Represents symbolic atoms
- **ValueAtom**: Stores actual values (strings, numbers, etc.)

#### 3. **Knowledge Graph Structure**

```python
# Risk Profile → Investment Types
metta.space().add_atom(E(S("risk_profile"), S("conservative"), S("bonds")))

# Investment Types → Expected Returns
metta.space().add_atom(E(S("expected_return"), S("bonds"), ValueAtom("3-5% annually")))

# Investment Types → Risk Levels
metta.space().add_atom(E(S("risk_level"), S("bonds"), ValueAtom("low risk, stable income")))
```

#### 4. **Querying with Pattern Matching**

```python
# Find investment types for risk profile
query_str = '!(match &self (risk_profile conservative $investment) $investment)'
results = metta.run(query_str)
```

### Key MeTTa Concepts

- **`&self`**: References the current space
- **`$variable`**: Pattern matching variables
- **`!(match ...)`**: Query syntax for pattern matching
- **`E(S(...), S(...), ...)`**: Creates logical expressions

For more detailed information about MeTTa, visit the [official documentation](https://metta-lang.dev/docs/learn/tutorials/python_use/metta_python_basics.html).

## 🏗️ Project Architecture

### Core Components

1. **`agent.py`**: Main Solana Portfolio Analyzer uAgent with dual protocols:
   - **Chat Protocol**: Human interaction via ASI:One
   - **Trading Protocol**: Agent-to-agent PriceRequest/TradeSignal communication
2. **`knowledge.py`**: MeTTa knowledge graph with Solana ecosystem data
3. **`investment_rag.py`**: Solana Portfolio RAG system for token analysis
4. **`utils.py`**: Trading signal generation and portfolio analysis logic

### Data Flow

#### For Chat Interface:

User Query → Intent Classification → MeTTa Query → Portfolio Analysis → LLM Response → User

#### For Agent Communication:

PriceRequest → Portfolio Analysis → Trading Signal Generation → TradeSignal Response

## 🔧 Integration with uAgents

### Using This as a Template

This project serves as a template for integrating MeTTa with uAgents. The key integration point is the `process_query` function in `utils.py`, which you can customize for your specific use case.

### Customization Steps

1. **Extend Solana Knowledge** (`knowledge.py`):

   ```python
   def initialize_solana_knowledge(metta: MeTTa):
       # Add new Solana tokens and protocols
       metta.space().add_atom(E(S("token_category"), S("defi"), S("YOUR_TOKEN")))
       metta.space().add_atom(E(S("protocol"), S("your_protocol"), S("YOUR_TOKEN")))
   ```

2. **Update Trading Logic** (`utils.py`):

   ```python
   def process_trading_data(price_data, rag: SolanaPortfolioRAG):
       # Implement your custom trading signal logic
       token = price_data.get("token")
       # Add your custom analysis here
   ```

3. **Extend Portfolio Analysis** (`investment_rag.py`):

   ```python
   class SolanaPortfolioRAG:
       def __init__(self, metta_instance: MeTTa):
           self.metta = metta_instance

       def analyze_your_metric(self, metric):
           # Implement custom portfolio metrics
           query_str = f'!(match &self (your_metric {metric} $result) $result)'
           return self.metta.run(query_str)
   ```

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.11+
- ASI:One API key

### Installation

1. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd financial-advisor-agent
   ```

2. **Create virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   To get the ASI:One API Key, login to https://asi1.ai/ and go to **Developer** section, click on **Create New** and copy your API Key. Please refer this [guide](https://innovationlab.fetch.ai/resources/docs/asione/asi-one-quickstart#step-1-get-your-api-key) for detailed steps.

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the agent**:
   ```bash
   python agent.py
   ```

### Environment Variables

Create a `.env` file with:

```env
ASI_ONE_API_KEY=your_asi_one_api_key_here
```

## 💡 Key Features

### 1. **Dual Protocol Support**

The agent supports both human and agent communication:

```python
# Agent-to-agent trading signals
@agent.on_message(model=PriceRequest)
async def handle_price_request(ctx: Context, sender: str, msg: PriceRequest):
    signal_result = process_trading_data(price_data, rag)
    await ctx.send(sender, TradeSignal(signal=signal_result["signal"], percent=signal_result["percent"]))

# Human chat interface
@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    response = process_chat_query(user_query, rag, llm)
```

### 2. **Solana-Specific Analysis**

Uses ASI:One to classify trading queries and analyze Solana portfolios:

- `portfolio_analysis`: Comprehensive portfolio evaluation
- `token_analysis`: Individual Solana token assessment
- `trading_signal`: Market condition-based recommendations
- `risk_assessment`: Portfolio risk evaluation
- `protocol_info`: DeFi protocol analysis

### 3. **Advanced Trading Signals**

MeTTa enables sophisticated trading logic:

```python
# Generate trading signals based on multiple factors
signal_result = rag.generate_trading_signal(
    token, current_price, entry_price, historical_prices, holdings_pct
)
# Returns: {"signal": "BUY", "percent": 15, "analysis": {...}}
```

### 4. **Dynamic Portfolio Learning**

The agent can learn about new Solana tokens and protocols:

```python
# Automatically adds new Solana knowledge when encountered
rag.add_knowledge("token_category", "NEW_TOKEN", "defi")
rag.add_knowledge("protocol", "new_protocol", "PROTOCOL_TOKEN")
```

### 5. **Agentverse Integration**

The agent automatically:

- Registers on Agentverse for discovery
- Implements dual protocols for versatile interaction
- Provides trading signal API for other agents
- Offers chat interface for human portfolio analysis

## 🧪 Testing the Agent

1. **Start the agent**:

   ```bash
   python agent.py
   ```

2. **Access the inspector**:
   Visit the URL shown in the console (e.g., `https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8008&address=agent1qd674kgs3987yh84a309c0lzkuzjujfufwxslpzygcnwnycjs0ppuauektt`) and click on `Connect` and select the `Mailbox` option. For detailed steps for connecting Agents via Mailbox, please refer [here](https://innovationlab.fetch.ai/resources/docs/agent-creation/uagent-creation#mailbox-agents).

3. **Test queries**:

### 🎯 Portfolio Analysis & Risk Assessment

- "Analyze my Solana portfolio with 50% SOL, 30% RAY, 20% USDC"
- "What's the risk level of holding mainly DeFi tokens?"
- "How should I rebalance my portfolio for conservative risk?"

### 💰 Token Analysis & Performance

- "What's your analysis of RAY token performance?"
- "Is ORCA a good investment for DeFi exposure?"
- "What category does JUP token fall into?"

### 📊 Trading Signals & Market Conditions

- "What's the trading signal for oversold conditions?"
- "Should I buy, sell, or hold in a bear market?"
- "What allocation strategy works best in sideways markets?"

### 🎯 DeFi Protocol Information

- "Tell me about Raydium protocol and its token"
- "What tokens are associated with major Solana DEXs?"
- "Which DeFi protocols offer the best risk-reward?"

### 📈 Solana Ecosystem Insights

- "What are the blue chip tokens in Solana ecosystem?"
- "How volatile are Solana meme coins typically?"
- "What's the recommended SOL allocation percentage?"

### ⚠️ Trading Mistakes & Risk Management

- "What are common mistakes when trading Solana tokens?"
- "How much should I allocate to meme coins?"
- "Why shouldn't I FOMO into new Solana launches?"

### Agent-to-Agent Communication

For programmatic trading signal generation, send PriceRequest messages:

```python
price_request = PriceRequest(
    token="SOL",
    current_price=180.5,
    entry_price=150.0,
    historical_prices=[140, 150, 160, 170, 180],
    current_holdings=25.0
)
# Agent responds with TradeSignal(signal="BUY", percent=15.0)
```

## Test Agents using Chat with Agent button on Agentverse

1. Once the agent is connected via Mailbox, go to `Agent Profile` and click on `Chat with Agent`

2. Interact with your agent through the Agentverse chat interface and try sample queries like:

   - "I'm a conservative investor, what should I invest in?"
   - "What returns can I expect from bonds?"
   - "How should a 30-year-old allocate their portfolio?"

3. The agent will use MeTTa knowledge graphs to provide structured investment advice based on:

   - Risk profile analysis
   - Expected return calculations
   - Age-appropriate allocation strategies
   - Goal-oriented planning

4. Agent terminal logs will show intent classification and knowledge retrieval from the MeTTa graph

5. Test the agent with ASI:One platform for Solana portfolio queries

6. **Agent-to-Agent Testing**: Use the client.py to send PriceRequest messages and receive TradeSignal responses for automated trading integration.

## 📊 Solana Knowledge Graph Structure

The MeTTa knowledge graph contains Solana ecosystem relationships:

- **Token Categories** → Tokens (blue_chip → SOL, defi → RAY, meme → WIF)
- **Tokens** → Volatility Levels (SOL → "high", BONK → "extreme")
- **Tokens** → Market Cap Tiers (RAY → "mid_cap", USDC → "large_cap")
- **Protocols** → Associated Tokens (raydium → RAY, orca → ORCA)
- **Signal Conditions** → Trading Actions (oversold → "BUY", overbought → "SELL")
- **Risk Levels** → Portfolio Allocations (moderate → "50% SOL, 30% DeFi, 20% stables")
- **Market Conditions** → Strategies (bear_market → "increase stables, DCA blue chips")
- **Trading Mistakes** → Warnings (ape_into_memes → "limit meme allocation to 5-10% max")

## 🔗 Useful Links

- [MeTTa Documentation](https://metta-lang.dev/docs/learn/tutorials/python_use/metta_python_basics.html)
- [Fetch.ai uAgents](https://innovationlab.fetch.ai/resources/docs/examples/chat-protocol/asi-compatible-uagents)
- [Agentverse](https://agentverse.ai/)
- [ASI:One](https://asi1.ai/)
