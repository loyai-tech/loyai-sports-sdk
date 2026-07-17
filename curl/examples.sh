#!/usr/bin/env bash
# LoyAI Sports Intelligence API — cURL Examples
# Docs:  https://loyaisportsintelligenceapi.com/docs
# Spec:  https://loyaisportsintelligenceapi.com/api/redoc
# Keys:  https://loyaisportsintelligenceapi.com/dashboard

API_KEY="YOUR_API_KEY_HERE"
BASE="https://loyaisportsintelligenceapi.com/api/v1"

# ── Health check (no auth required) ──────────────────────────────────────────
echo "=== Health Check ==="
curl -s "$BASE/../healthz" | jq .

# ── List active sports ────────────────────────────────────────────────────────
echo -e "\n=== Active Sports ==="
curl -s -H "x-api-key: $API_KEY" \
  "$BASE/sports" | jq '[.[] | {key, title, active}]'

# ── MLB moneyline odds ────────────────────────────────────────────────────────
echo -e "\n=== MLB Moneyline Odds ==="
curl -s -H "x-api-key: $API_KEY" \
  "$BASE/sports/baseball_mlb/odds?markets=h2h" | jq '.events[0]'

# ── MLB spreads + totals ──────────────────────────────────────────────────────
echo -e "\n=== MLB Spreads & Totals ==="
curl -s -H "x-api-key: $API_KEY" \
  "$BASE/sports/baseball_mlb/odds?markets=spreads,totals" | jq '.events[0]'

# ── Multi-book odds (DraftKings + FanDuel) ────────────────────────────────────
echo -e "\n=== Multi-book Odds ==="
curl -s -H "x-api-key: $API_KEY" \
  "$BASE/sports/baseball_mlb/book-odds?books=draftkings,fanduel" | jq '.games[0]'

# ── Expected value analysis ───────────────────────────────────────────────────
echo -e "\n=== EV Analysis (top 3) ==="
curl -s -H "x-api-key: $API_KEY" \
  "$BASE/sports/baseball_mlb/ev" | jq '.picks[:3]'

# ── Player props EV ───────────────────────────────────────────────────────────
echo -e "\n=== Props EV (top 3) ==="
curl -s -H "x-api-key: $API_KEY" \
  "$BASE/sports/baseball_mlb/props-ev" | jq '.picks[:3]'

# ── Scores ────────────────────────────────────────────────────────────────────
echo -e "\n=== Scores ==="
curl -s -H "x-api-key: $API_KEY" \
  "$BASE/sports/baseball_mlb/scores?daysFrom=1" | jq '.scores[:2]'

# ── Parlay Lab ────────────────────────────────────────────────────────────────
echo -e "\n=== Parlay Lab Picks ==="
curl -s -H "x-api-key: $API_KEY" \
  "$BASE/parlay-lab/picks?sport=baseball_mlb&legs=3" | jq '.parlays[0]'

# ── AI Assist (Basic plan+ required, costs 50 quota) ──────────────────────────
echo -e "\n=== AI Assist ==="
curl -s -H "x-api-key: $API_KEY" \
  "$BASE/ai/assist?q=Which+MLB+bets+have+the+best+value+today&sport=baseball_mlb" | jq .

# ── Key management ────────────────────────────────────────────────────────────
echo -e "\n=== Key Info ==="
curl -s -H "x-api-key: $API_KEY" \
  "$BASE/../v1/keys/me" | jq '{plan, quota, requests_used, requests_remaining}'
