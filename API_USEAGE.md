# ASI:One Agent API - Usage Guide

## 🌐 Public Endpoints

Your Flask app now has three public API endpoints that anyone can use:

### Base URL

```
http://your-server-ip:5000
```

---

## 📡 API Endpoints

### 1. **POST /api/query** - Submit a Query

Send a question to the agent and optionally wait for the response.

#### Request

```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I bought 3 SOL at $20, should I sell and buy ETH?",
    "wait_for_response": false
  }'
```

#### Parameters

- `query` (string, required) - Your question for the agent
- `wait_for_response` (boolean, optional) - If `true`, waits up to 60 seconds for the response. Default: `false`

#### Response (Async - wait_for_response: false)

```json
{
  "success": true,
  "message_id": "fa917acb-ead0-4539-994e-6de0f5e6dfec",
  "status": "queued",
  "query": "I bought 3 SOL at $20, should I sell and buy ETH?"
}
```

#### Response (Sync - wait_for_response: true)

```json
{
  "success": true,
  "message_id": "fa917acb-ead0-4539-994e-6de0f5e6dfec",
  "status": "complete",
  "query": "I bought 3 SOL at $20, should I sell and buy ETH?",
  "response": "**Professional Solana (SOL) Portfolio Analysis...",
  "completed_at": "2025-11-28T02:44:35.123456"
}
```

---

### 2. **GET /api/response/{message_id}** - Get Response

Retrieve the response for a previously submitted query.

#### Request

```bash
curl http://localhost:5000/api/response/fa917acb-ead0-4539-994e-6de0f5e6dfec
```

#### Response (Complete)

```json
{
  "success": true,
  "message_id": "fa917acb-ead0-4539-994e-6de0f5e6dfec",
  "status": "complete",
  "response": "**Professional Solana (SOL) Portfolio Analysis...",
  "completed_at": "2025-11-28T02:44:35.123456"
}
```

#### Response (Pending)

```json
{
  "success": true,
  "message_id": "fa917acb-ead0-4539-994e-6de0f5e6dfec",
  "status": "acknowledged",
  "query": "I bought 3 SOL at $20, should I sell and buy ETH?",
  "queued_at": "2025-11-28T02:44:30.123456"
}
```

---

### 3. **GET /api/docs** - API Documentation

View complete API documentation in your browser or via curl.

#### Request

```bash
curl http://localhost:5000/api/docs
```

Or visit in browser: `http://localhost:5000/api/docs`

---

## 💻 Code Examples

### Python

```python
import requests
import time

# Async approach (non-blocking)
def query_agent_async(query):
    response = requests.post(
        'http://localhost:5000/api/query',
        json={'query': query}
    )
    data = response.json()
    message_id = data['message_id']

    # Poll for response
    while True:
        result = requests.get(f'http://localhost:5000/api/response/{message_id}')
        result_data = result.json()

        if result_data['status'] == 'complete':
            return result_data['response']

        time.sleep(1)

# Sync approach (blocking)
def query_agent_sync(query):
    response = requests.post(
        'http://localhost:5000/api/query',
        json={
            'query': query,
            'wait_for_response': True
        }
    )
    data = response.json()
    return data.get('response', 'No response received')

# Usage
answer = query_agent_sync("Should I invest in DeFi tokens?")
print(answer)
```

### JavaScript/Node.js

```javascript
const axios = require("axios");

// Async approach
async function queryAgentAsync(query) {
  const response = await axios.post("http://localhost:5000/api/query", {
    query: query,
  });

  const messageId = response.data.message_id;

  // Poll for response
  while (true) {
    const result = await axios.get(
      `http://localhost:5000/api/response/${messageId}`
    );

    if (result.data.status === "complete") {
      return result.data.response;
    }

    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
}

// Sync approach
async function queryAgentSync(query) {
  const response = await axios.post("http://localhost:5000/api/query", {
    query: query,
    wait_for_response: true,
  });

  return response.data.response;
}

// Usage
(async () => {
  const answer = await queryAgentSync("Should I invest in DeFi tokens?");
  console.log(answer);
})();
```

### cURL Examples

```bash
# Async query
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the best DeFi protocols?"}'

# Sync query (wait for response)
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the best DeFi protocols?", "wait_for_response": true}'

# Get response by message ID
curl http://localhost:5000/api/response/YOUR-MESSAGE-ID-HERE
```

---

## 🌍 Making It Accessible from Anywhere

### Option 1: Deploy to a Cloud Server

Deploy your Flask app to:

- **AWS EC2** / **Google Cloud** / **Azure VM**
- **DigitalOcean Droplet**
- **Heroku** / **Railway** / **Render**

Then your API will be accessible at:

```
http://your-server-ip:5000/api/query
```

### Option 2: Use ngrok (Quick Testing)

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com

# Run ngrok
ngrok http 5000

# You'll get a public URL like:
# https://abc123.ngrok.io
```

Then anyone can access:

```
https://abc123.ngrok.io/api/query
```

### Option 3: Use Cloudflare Tunnel

```bash
# Install cloudflared
brew install cloudflare/cloudflare/cloudflared

# Create tunnel
cloudflared tunnel --url http://localhost:5000
```

---

## 🔒 Security Considerations

For production use, consider adding:

1. **API Key Authentication**
2. **Rate Limiting**
3. **CORS Configuration**
4. **HTTPS/SSL**
5. **Input Validation**

Example with API key:

```python
API_KEY = "your-secret-api-key"

@app.route('/api/query', methods=['POST'])
def api_query():
    auth_header = request.headers.get('Authorization')
    if auth_header != f'Bearer {API_KEY}':
        return jsonify({'error': 'Unauthorized'}), 401
    # ... rest of the code
```

---

## 📊 Status Codes

- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found (invalid message ID)
- `500` - Server Error

---

## 🎯 Use Cases

1. **Mobile Apps** - Query the agent from iOS/Android apps
2. **Web Apps** - Integrate into React/Vue/Angular frontends
3. **Discord/Telegram Bots** - Create chatbots that use your agent
4. **Automation Scripts** - Schedule periodic queries
5. **Analytics Dashboards** - Display agent insights in real-time

---

## 🔧 Testing

Test the API is working:

```bash
curl http://localhost:5000/api/docs
```

You should see the full API documentation in JSON format.
