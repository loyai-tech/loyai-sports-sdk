/**
 * LoyAI Sports Intelligence API — Node.js / TypeScript SDK Boilerplate
 * Docs: https://loyaisportsintelligenceapi.com/docs
 * Spec: https://loyaisportsintelligenceapi.com/api/redoc
 *
 * Install: no extra dependencies — uses the native fetch API (Node 18+)
 */

const BASE_URL = "https://loyaisportsintelligenceapi.com/api/v1";

interface RequestOptions {
  params?: Record<string, string | number | boolean>;
}

export class LoyAIClient {
  private headers: HeadersInit;

  constructor(private apiKey: string) {
    this.headers = {
      "x-api-key": apiKey,
      Accept: "application/json",
      "User-Agent": "loyai-node-sdk/1.0",
    };
  }

  private async get<T = unknown>(path: string, opts: RequestOptions = {}): Promise<T> {
    const url = new URL(`${BASE_URL}${path}`);
    for (const [k, v] of Object.entries(opts.params ?? {})) {
      url.searchParams.set(k, String(v));
    }
    const res = await fetch(url.toString(), { headers: this.headers });
    if (!res.ok) {
      const body = await res.text();
      throw new Error(`LoyAI API error ${res.status}: ${body}`);
    }
    return res.json() as Promise<T>;
  }

  /** List all supported sports. Pass all=true to include off-season leagues. */
  getSports(all = false) {
    return this.get<unknown[]>("/sports", { params: { all } });
  }

  /**
   * Get live odds for a sport.
   * @param sportKey  e.g. "baseball_mlb", "americanfootball_nfl"
   * @param markets   "h2h" | "spreads" | "totals" (comma-separated)
   */
  getOdds(sportKey: string, markets = "h2h") {
    return this.get("/sports/:sportKey/odds".replace(":sportKey", sportKey), {
      params: { markets },
    });
  }

  /**
   * Get odds from multiple sportsbooks side-by-side.
   * @param books  Array of book keys e.g. ["draftkings", "fanduel", "betmgm"]
   */
  getBookOdds(sportKey: string, books?: string[]) {
    return this.get(`/sports/${sportKey}/book-odds`, {
      params: books ? { books: books.join(",") } : {},
    });
  }

  /** Expected value (EV) analysis for all games in a sport. */
  getEV(sportKey: string) {
    return this.get(`/sports/${sportKey}/ev`);
  }

  /** EV-ranked player props for a sport. */
  getPropsEV(sportKey: string) {
    return this.get(`/sports/${sportKey}/props-ev`);
  }

  /** Live and completed scores. */
  getScores(sportKey: string, daysFrom = 1) {
    return this.get(`/sports/${sportKey}/scores`, { params: { daysFrom } });
  }

  /** Upcoming events for a sport. */
  getEvents(sportKey: string) {
    return this.get(`/sports/${sportKey}/events`);
  }

  /**
   * Natural-language AI assistant for sports betting questions.
   * Requires Basic plan or above. Costs 50 quota units per call.
   */
  aiAssist(query: string, sport = "baseball_mlb") {
    return this.get("/ai/assist", { params: { q: query, sport } });
  }
}

// ── Quick example ─────────────────────────────────────────────────────────────

async function main() {
  const client = new LoyAIClient("YOUR_API_KEY_HERE");

  const sports = await client.getSports();
  console.log("Active sports:", (sports as Array<{ title: string }>).map((s) => s.title));

  const odds = await client.getOdds("baseball_mlb", "h2h,spreads,totals");
  console.log("MLB odds:", JSON.stringify(odds, null, 2).slice(0, 500) + "…");

  const bookOdds = await client.getBookOdds("baseball_mlb", ["draftkings", "fanduel"]);
  console.log("Book odds:", JSON.stringify(bookOdds, null, 2).slice(0, 300) + "…");
}

main().catch(console.error);
