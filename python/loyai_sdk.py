"""
LoyAI Sports Intelligence API — Python SDK Boilerplate
Docs: https://loyaisportsintelligenceapi.com/docs
Spec: https://loyaisportsintelligenceapi.com/api/redoc
"""

import requests
from typing import Optional

BASE_URL = "https://loyaisportsintelligenceapi.com/api/v1"


class LoyAIClient:
    """Minimal Python client for the LoyAI Sports Intelligence API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": api_key,
            "Accept": "application/json",
            "User-Agent": "loyai-python-sdk/1.0",
        })

    def _get(self, path: str, params: Optional[dict] = None) -> dict:
        url = f"{BASE_URL}{path}"
        resp = self.session.get(url, params=params or {})
        resp.raise_for_status()
        return resp.json()

    # ── Sports ──────────────────────────────────────────────────────────────

    def get_sports(self, all: bool = False) -> list[dict]:
        """List all supported sports. Pass all=True to include off-season leagues."""
        return self._get("/sports", {"all": str(all).lower()})

    # ── Odds ────────────────────────────────────────────────────────────────

    def get_odds(self, sport_key: str, markets: str = "h2h") -> dict:
        """
        Get live moneyline (h2h), spread, and totals odds for a sport.

        sport_key examples: baseball_mlb, americanfootball_nfl, basketball_nba
        markets: "h2h" | "spreads" | "totals" (comma-separated for multiple)
        """
        return self._get(f"/sports/{sport_key}/odds", {"markets": markets})

    # ── Multi-book Odds ──────────────────────────────────────────────────────

    def get_book_odds(self, sport_key: str, books: Optional[list[str]] = None) -> dict:
        """
        Get odds from multiple sportsbooks side-by-side.

        books: list of book keys e.g. ["draftkings", "fanduel", "betmgm"]
               defaults to all available books
        """
        params = {}
        if books:
            params["books"] = ",".join(books)
        return self._get(f"/sports/{sport_key}/book-odds", params)

    # ── Expected Value ───────────────────────────────────────────────────────

    def get_ev(self, sport_key: str) -> dict:
        """Get expected value (EV) analysis for all games in a sport."""
        return self._get(f"/sports/{sport_key}/ev")

    # ── Player Props ─────────────────────────────────────────────────────────

    def get_props_ev(self, sport_key: str) -> dict:
        """Get EV-ranked player props for a sport."""
        return self._get(f"/sports/{sport_key}/props-ev")

    # ── Scores ───────────────────────────────────────────────────────────────

    def get_scores(self, sport_key: str, days_from: int = 1) -> dict:
        """Get live and completed scores."""
        return self._get(f"/sports/{sport_key}/scores", {"daysFrom": days_from})

    # ── Events ───────────────────────────────────────────────────────────────

    def get_events(self, sport_key: str) -> dict:
        """Get upcoming events for a sport."""
        return self._get(f"/sports/{sport_key}/events")

    # ── AI Assist ────────────────────────────────────────────────────────────

    def ai_assist(self, query: str, sport: str = "baseball_mlb") -> dict:
        """
        Ask a natural-language question about sports betting.
        Requires Basic plan or above. Counts as 50 quota units.
        """
        return self._get("/ai/assist", {"q": query, "sport": sport})


# ── Quick example ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    client = LoyAIClient(api_key="YOUR_API_KEY_HERE")

    # List active sports
    sports = client.get_sports()
    print("Active sports:", [s["title"] for s in sports])

    # Get MLB odds
    mlb_odds = client.get_odds("baseball_mlb", markets="h2h,spreads,totals")
    print(f"\nMLB odds — {len(mlb_odds.get('events', []))} games found")

    # Multi-book comparison
    book_odds = client.get_book_odds("baseball_mlb", books=["draftkings", "fanduel"])
    print(f"Book odds: {len(book_odds.get('games', []))} games")
