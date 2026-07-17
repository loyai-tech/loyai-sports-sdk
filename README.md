# LoyAI Sports Intelligence API — SDK Boilerplate

Quick-start code for the [LoyAI Sports Intelligence API](https://loyaisportsintelligenceapi.com).

## Documentation & Status

- **Interactive API Reference:** [Redoc Explorer](https://loyaisportsintelligenceapi.com/api/redoc)
- **System Operational Status:** [Live Uptime Status Page](https://loyaisportsintelligenceapi.com/status)
- **Human-Readable Docs:** [Documentation](https://loyaisportsintelligenceapi.com/docs)
- **RapidAPI Listing:** [loyai-sports-intelligence-api2.p.rapidapi.com](https://rapidapi.com/loyai-sports-intelligence-api2)

## Get an API Key

Free tier: 500 calls/month, no credit card required → [Dashboard](https://loyaisportsintelligenceapi.com/dashboard)

## Authentication

Pass your key as a header or query param:

```bash
# Header (recommended)
curl -H "x-api-key: YOUR_KEY" https://loyaisportsintelligenceapi.com/api/v1/sports

# Query param
curl "https://loyaisportsintelligenceapi.com/api/v1/sports?apiKey=YOUR_KEY"
```

## Quick Examples

### Python

```bash
pip install requests
python python/loyai_sdk.py
```

### Node.js / TypeScript

```bash
# No extra dependencies — requires Node 18+
npx tsx node/loyai-sdk.ts
```

### cURL

```bash
chmod +x curl/examples.sh
API_KEY=your_key ./curl/examples.sh
```

## Key Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/v1/sports` | List all supported sports |
| `GET /api/v1/sports/{sport}/odds` | Live moneyline, spread, totals |
| `GET /api/v1/sports/{sport}/book-odds` | Multi-book odds comparison |
| `GET /api/v1/sports/{sport}/ev` | Expected value analysis |
| `GET /api/v1/sports/{sport}/props-ev` | Player props EV |
| `GET /api/v1/sports/{sport}/scores` | Live + completed scores |
| `GET /api/v1/parlay-lab/picks` | AI-ranked parlay picks |
| `GET /api/v1/ai/assist` | Natural-language betting assistant |
| `GET /api/healthz` | Health check (no auth required) |

Full interactive reference: [https://loyaisportsintelligenceapi.com/api/redoc](https://loyaisportsintelligenceapi.com/api/redoc)

## GitHub Actions (CI skeleton)

Drop this in `.github/workflows/test.yml` to auto-verify the API is reachable on every push:

```yaml
name: Smoke Test
on: [push, pull_request]
jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Health check
        run: |
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://loyaisportsintelligenceapi.com/api/healthz)
          [ "$STATUS" = "200" ] && echo "API healthy" || (echo "API returned $STATUS"; exit 1)
      - name: Sports list check
        env:
          API_KEY: ${{ secrets.LOYAI_API_KEY }}
        run: |
          curl -sf -H "x-api-key: $API_KEY" \
            "https://loyaisportsintelligenceapi.com/api/v1/sports" | python3 -c "import sys,json; data=json.load(sys.stdin); print(f'Got {len(data)} sports')"
```

## License

MIT — free to use, modify, and redistribute.
