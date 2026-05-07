# Loop 9 — Win Criteria

You're done when:

- [ ] `caching.py` exists and the cache hit rate on load_test is measurable in `NOTES.md`.
- [ ] `retries.py` exists. load_test failure rate is dramatically lower than the broken-state baseline.
- [ ] `cost.py` tracks tokens + dollars. `/stats` endpoint returns session totals. Monthly projection at scale is in `NOTES.md`.
- [ ] `evals/run_offline.py` runs with bias-controlled judging (verbosity-ignoring + order-swap uncertainty). Pass-rate is measurable across runs.
- [ ] `injection_guards.py` exists with input scanner, output scanner, and one dual-LLM-protected risky tool. You can demonstrate an injection attempt being blocked.
- [ ] `observability.py` produces structured logs with trace IDs and the `/metrics` endpoint exposes prometheus counters.
- [ ] Streaming works on `/query` (or a streaming-only endpoint). TTFT vs total-latency comparison is in `NOTES.md`.
- [ ] At least one path in the agent is `async` with a parallel fan-out. You can name when async helped vs didn't.
- [ ] Secrets handling note in `NOTES.md` (key rotation procedure).
- [ ] The agent is **deployed** to a real provider (Cloud Run / Fly / Render). The HTTPS URL works and the cold-start time is in `NOTES.md`.
- [ ] Monitoring thresholds are written down (no need for PagerDuty — just the thresholds + what you'd do).
- [ ] Rate limiting + graceful degradation work (set an invalid key, server fails fast not hangs).
- [ ] Model selection trade-off table is in `NOTES.md`.

When all 13 are checked, finish `CHEATSHEET.md`. Then `/loop next` for Loop 10 — capstone, same Group D venv.

## Stretch (optional)

- Add a chaos-test script: every Nth request, simulate an API timeout / 500 / malformed response from the upstream. Watch the retry behavior.
- Add a circuit breaker (when 5 consecutive requests fail, open the circuit for 30s, return 503 fast).
- Build a simple admin dashboard (read-only) that pulls from `/metrics` and shows request rate / error rate / cost over time.
- Replace the in-process cache with Redis. Measure latency delta — is the network hop worth it?
- Profile the agent loop with `py-spy` or `cProfile` under load. Where is time actually spent? (Often: the LLM call dominates, but not always.)

## How the tutor will check

When you say you're done:
1. Server is running (locally or deployed). `curl /health` returns `{"status":"ok"}`.
2. Run `load_test.py` — see post-fix p50/p95/p99 latency dramatically better than broken-state baseline.
3. Hit `/stats` — see token + cost totals.
4. Hit `/metrics` — see prometheus counters populated.
5. Send an injection-attempt query — see it blocked at the input scanner.
6. Run `python evals/run_offline.py` — see pass-rate with bias-controlled judging.
7. Show the deployed URL.
8. Read aloud the model-selection table.

Behavior + measurement > implementation polish. Loop 9 isn't graded on code beauty; it's graded on numbers.
