# 🤖 fr-icm Trading Agent — Multi-Agent AI for Market Intelligence & Automated Trade Decisions

## 🧩 Overview

The **ICM Trading Agent** is a **multi-agent, AI-powered autonomous trading system** built to operate across **Fetch.ai’s Agentverse** and **ASI:One ecosystems**.

It enables **collaborative, intelligent trading decisions** by combining **local portfolio analytics** with **decentralized market gossip** from other AI agents — allowing your system to learn from collective intelligence and act on it automatically.

This gossip-based architecture empowers the agent to analyze both **real-time market signals** (trends, news, sentiment) and **local performance data** (historical prices, holdings, PnL) to determine whether to **buy**, **sell**, **hold**, or **DCA (dollar-cost average)** — with a calculated **allocation percentage**.

---

## 💡 Key Capabilities

- 🕸️ **Multi-Agent Communication** — Exchanges market insights and trade signals across Fetch.ai’s decentralized network and ASI:One.
- 🧩 **Agentverse Integration** — Fully compatible with the **Agentverse UI**, **uAgents SDK**, and **ASI:One chat interface** for human-in-the-loop control.
- 📊 **Portfolio Awareness** — Reads local price and position data for precise contextual reasoning.
- 🧠 **AI-Driven Decision Logic** — Computes signal strength using statistical models for adaptive trade calls.
- ⚙️ **Automated Signal Response** — Outputs structured trading actions that external bots or dashboards can directly execute.
- 🌍 **Interoperable by Design** — Runs on **uAgents**, supports **cross-ecosystem communication** via the Fetch.ai agent protocol.

---

## 🧭 Example Use Cases

### 1. Autonomous Portfolio Adjustment

A local analytics agent sends pool and token metrics to the gossip agent.
The gossip agent replies with actionable advice, e.g. **“BUY 15%”**, triggering automated rebalancing.

### 2. Sentiment-Driven Strategy

When peer agents on Fetch.ai or ASI:One report bearish sentiment, the trading agent adapts by issuing **“HOLD”** or **“REDUCE EXPOSURE”** instructions.

### 3. Cross-Network Intelligence

Aggregates multi-source intelligence from on-chain data and connected agents, improving collective decision accuracy.

---

## 🔌 Capabilities & APIs

### Supported Message Models

| Model            | Description                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| **PriceRequest** | Contains local token data (current price, entry, historicals, holdings). |
| **TradeSignal**  | Response containing recommended action and capital allocation.           |

### Message Flow

1. **Local Agent → Gossip Agent:** Sends `PriceRequest`
2. **Gossip Agent → Local Agent:** Returns `TradeSignal` (e.g. `BUY 15%`)
3. **Executor (optional):** Executes the trade on supported DEX/ICM infra

---

### Example Interaction

**Request**

```json
{
  "token": "RAY",
  "current_price": 0.35,
  "entry_price": 0.4,
  "historical_prices": [0.42, 0.38, 0.36, 0.35],
  "current_holdings": 25
}
```

**Response**

```json
{
  "signal": "BUY",
  "percent": 15.0
}
```

---

## ⚙️ Implementation Summary

The gossip agent employs **statistical reasoning** for adaptive decision making:

- **DCA** — when unrealized loss < -10% and holdings < 50%
- **SELL** — when unrealized profit > 10% and holdings > 10%
- **BUY** — when current price < historical mean
- **SELL** — when current price > historical mean
- **HOLD** — otherwise

This logic enables robust autonomous operations without deep-learning retraining cycles.

---

## 💬 Chat Interface (ASI:One)

The agent can also be deployed as a **chat-enabled uAgent** inside **ASI:One**, allowing direct interaction through human text commands.

### Example (Chat Workflow)

1. User opens ASI:One chat → “Analyze SOL pool data”
2. The agent parses text, runs portfolio analysis
3. It replies with structured advice like:

   ```
   Current PnL: -12%
   Suggested Action: DCA 20%
   ```

4. Response is delivered back to the ASI:One chat UI in real time.

This mode is powered by:

```python
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent
```

and includes support for session handling and acknowledgements.

---

## 🧠 Interaction Modes

- **Agent-to-Agent Messaging** — Peer communication within Fetch.ai or ASI:One.
- **Chat Protocol Interface** — Human text interaction within the ASI:One UI.
- **Local or API Integration** — Embeddable in trading infrastructure or dashboards.

---

## 🚫 Limitations & Scope

- Does **not** execute real trades — only emits **signals**.
- Requires **external market data** or an analytics agent.
- Uses **rule-based** reasoning (no neural inference yet).
- **Optional** manual control through ASI:One or REST API.

---

## 🔍 Keywords & Tags

`autonomous trading`, `multi-agent intelligence`, `gossip protocol`,
`Fetch.ai`, `ASI:One`, `Agentverse`, `uAgents`, `DeFi AI`,
`crypto analytics`, `ICM`, `portfolio signals`, `AI trading bot`

---

## 🧾 License

This project is licensed under the **MIT License**.
See the `LICENSE` file for full terms.

---

## 💬 Contact

- **Project Repository:** [github.com/OkarFabianTheWise/fr-icm-uagent](https://github.com/OkarFabianTheWise/fr-icm-uagent)
- **Ecosystem:** [Agentverse.io](https://agentverse.ai) | [ASI:One](https://asi.one) | [Fetch.ai](https://fetch.ai)

---

> _Built for the decentralized trading era — where AI agents learn, share, and trade together._

![tag](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag](https://img.shields.io/badge/hackathon-5F43F1)
