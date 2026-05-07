"""Loop 9 starter — FastAPI agent server, no production hardening.

This is what most agents look like the day they "ship." It works under low
load, in dev environments, when the upstream API is happy. It will embarrass
you the first time anything goes wrong.

Run:    uvicorn app:app --reload --port 8000
Test:   curl -X POST localhost:8000/query -H 'content-type: application/json' -d '{"question":"what is 12+7?"}'
Load:   python load_test.py
Read:   BREAK.md
"""
from fastapi import FastAPI
from pydantic import BaseModel

import agent

app = FastAPI(title="Loop 9 Agent (broken)")


class Query(BaseModel):
    question: str


class Reply(BaseModel):
    answer: str
    tokens: int
    tool_calls: int


@app.post("/query", response_model=Reply)
def query(req: Query) -> Reply:
    result = agent.answer(req.question)
    return Reply(**result)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
