# <Project name>

*One-sentence elevator pitch.*

## What it does

2–3 sentences. Concrete. Replace generic "an AI agent that..." with the specific job-to-be-done.

## Deployed URL

`https://<your-deployed-instance>` — try it: `curl -X POST <url>/query -H 'content-type: application/json' -d '{"question":"..."}'`

(Or for batch agents, four commands: `git clone <url>`, `cd <repo>`, `uv sync`, `uv run python run.py samples/`.)

## Quickstart (run locally)

```bash
git clone <url>
cd <project>
cp .env.example .env  # or set GEMINI_API_KEY in your environment

# Preferred (if your project ships the curriculum setup scripts):
python setup/bootstrap.py
python setup/group_env.py --group <X> --run python run.py samples/

# Legacy fallback:
cd exercises/group-<X>
uv sync
uv run python run.py samples/
```

## Architecture

Mermaid or ASCII sketch. ~5 boxes max:

```
[user] -> [API endpoint] -> [agent loop] -> [retrieval] -> [LLM] -> [response]
                                  |
                                  v
                              [tools]
```

Two-paragraph description of how it works. Include which Loop's patterns you reused.

## Eval results

20 cases in `evals/cases.json`. Run with `python evals/run_offline.py`.

| Metric | Value |
|---|---|
| Pass rate | __% |
| Numeric scorer cases | _N_ pass / _M_ total |
| Judge scorer cases | _N_ pass / _M_ total |
| Avg latency per case | _N_ ms |
| Total tokens for full eval run | _N_ |

## Cost

| Per single request | _N_ tokens (~_X_ ¢) |
|---|---|
| Per 1K requests | ~$_X_ |
| Per 100K requests | ~$_X_ |

Calculation based on `gemini-2.0-flash` pricing as of <date>.

## Production hardening (which Loop-9 stages are wired)

- [ ] Caching
- [ ] Retries with backoff
- [ ] Cost tracking
- [ ] Eval harness
- [ ] Injection guards
- [ ] Observability (`/metrics`)
- [ ] Streaming
- [ ] Async / parallel
- [ ] Rate limiting

You won't have all of these. Check the ones that *are* wired and write a sentence on why those mattered for this project.

## Limitations

3–5 honest bullets. Examples:
- Single-turn only (no chat history yet).
- Mocked external API; real integration is v2.
- Eval covers happy-path queries; adversarial queries not yet tested.

## License

(Optional: MIT, Apache, or omitted.)
