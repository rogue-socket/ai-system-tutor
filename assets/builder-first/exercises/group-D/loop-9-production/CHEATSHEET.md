# Loop 9 — Cheatsheet

*Fill in as you build.*

## Commands

- `uvicorn app:app --port 8000 --reload` — run server (dev)
- `python load_test.py` — concurrent load
- `python evals/run_offline.py` — offline eval
- `curl localhost:8000/health` — health check
- `curl localhost:8000/stats` — session totals (Stage 3)
- `curl localhost:8000/metrics` — prometheus (Stage 6)
- `docker build -t loop-9 . && docker run -p 8000:8000 -e GEMINI_API_KEY=$GEMINI_API_KEY loop-9` — local docker
- `gcloud run deploy ... --source .` — Cloud Run deploy

## Patterns

3–5 reusable code snippets. Suggestions:

- The retry decorator with exponential backoff + jitter.
- The token-bucket rate limiter or `slowapi` shape.
- The streaming endpoint pattern with `is_disconnected()` polling.
- The dual-LLM "trusted reviewer" wrapper for risky tools.
- The trace-ID-per-request middleware pattern.
- The `make_asgi_app()` mount for prometheus `/metrics`.

## Gotchas

3–5 traps. Suggestions:

- Bimodal latency: p50 1.5s, p99 60s. Picking *one* timeout is a trade-off, not a setting.
- Caching answers in memory loses them on restart. Redis or persistent store for any real workload.
- Judge bias: a same-model judge agrees with the answerer more than truth justifies. Cross-model judge mitigates.
- `is_disconnected()` doesn't always fire — TCP semantics, client behavior.
- `prometheus-client` counters are global; multi-worker uvicorn complicates per-worker accounting (use multiprocess mode).
- Cloud Run cold starts vary 0.5-5s. If you need sub-second always-on, set min instances ≥ 1 (costs).

## Numbers

Suggestions:

- Cache hit rate on load_test: _N_%.
- Success rate before / after retries: _N_% / _M_%.
- p50/p95/p99 broken vs fixed: _a_/_b_/_c_ → _A_/_B_/_C_ ms.
- Cost per load_test run (broken): $_x_; (with cache): $_y_.
- Monthly cost projection at 1000 RPS sustained: $_N_K.
- Eval pass rate: broken judge _x_%, bias-controlled judge _y_%.
- TTFT vs total latency, streaming: _a_ ms vs _b_ ms.
- Cold start on cloud provider: ~_N_ ms.
