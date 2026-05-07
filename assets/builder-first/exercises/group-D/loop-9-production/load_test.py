"""Hammer the FastAPI server with concurrent requests to surface failures.

Run the server first:
    uvicorn app:app --port 8000

Then:
    python load_test.py
"""
import asyncio
import time

import httpx

URL = "http://localhost:8000/query"
QUESTIONS = [
    "what is 12 + 7?",
    "multiply 9 by 11",
    "what's 25% of 80?",
    "compute 100 - 33",
    "divide 144 by 12",
    "what is 2 to the 8th power?",
    "what's the capital of France?",
    "tell me a joke about distributed systems",
    "compute 0.1 + 0.2 (be careful)",
    "what is x if x + 7 = 15?",
]
TOTAL_REQUESTS = 30
CONCURRENCY = 5


async def hit_once(client: httpx.AsyncClient, q: str, idx: int) -> dict:
    start = time.perf_counter()
    try:
        r = await client.post(URL, json={"question": q}, timeout=60)
        elapsed = (time.perf_counter() - start) * 1000
        return {"idx": idx, "ok": r.status_code == 200, "ms": elapsed, "status": r.status_code}
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        return {"idx": idx, "ok": False, "ms": elapsed, "error": f"{type(e).__name__}: {e}"}


async def main() -> None:
    async with httpx.AsyncClient() as client:
        sem = asyncio.Semaphore(CONCURRENCY)

        async def bound(q: str, i: int) -> dict:
            async with sem:
                return await hit_once(client, q, i)

        tasks = [bound(QUESTIONS[i % len(QUESTIONS)], i) for i in range(TOTAL_REQUESTS)]
        start = time.perf_counter()
        results = await asyncio.gather(*tasks)
        total_s = time.perf_counter() - start

    ok = [r for r in results if r["ok"]]
    fail = [r for r in results if not r["ok"]]
    latencies = sorted(r["ms"] for r in ok)

    def pct(p: float) -> float:
        if not latencies:
            return 0.0
        idx = max(0, min(len(latencies) - 1, int(len(latencies) * p)))
        return latencies[idx]

    print(f"\n=== Load test: {TOTAL_REQUESTS} req, concurrency {CONCURRENCY} ===")
    print(f"Total time: {total_s:.1f}s ({TOTAL_REQUESTS / total_s:.1f} req/s)")
    print(f"Success:    {len(ok)}/{TOTAL_REQUESTS}")
    print(f"Failures:   {len(fail)}")
    if latencies:
        print(f"Latency p50: {pct(0.5):.0f} ms")
        print(f"Latency p95: {pct(0.95):.0f} ms")
        print(f"Latency p99: {pct(0.99):.0f} ms")
    if fail:
        print("Sample failures:")
        for r in fail[:5]:
            print(f"  [{r.get('status', 'X')}] {r.get('error', '')}")


if __name__ == "__main__":
    asyncio.run(main())
