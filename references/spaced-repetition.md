# Spaced repetition

The skill maintains an SR queue in `progress.json`. Items get rescheduled by an SM-2-lite algorithm based on the learner's response quality. Daily review nudges questions back to long-term retention.

---

## When items enter the queue

- **Diagnostic miss.** The learner answered a diagnostic question wrong or shakily — that question becomes an SR item, due in 1 day.
- **Auto-quiz miss.** Mid-lesson quiz answered wrong — SR entry, due in 1 day.
- **Lesson key fact.** At the end of a lesson, the skill picks 2-3 "must-remember" facts (the ones the lesson hinged on). They become SR items, due in 2 days.
- **Self-flagged.** The learner says "I want to remember this" — SR entry, due in 1 day.
- **Reflection insight.** A surprise from `reflection.md` after an exercise becomes an SR item, due in 3 days.

Don't let the queue grow without bound. Cap at ~50 active items per layer. If the learner is consistently missing the same item across 4+ reviews, it's a foundational gap — surface it as a topic to re-teach, not just an SR item to retry.

---

## SR item schema

Stored at `progress.json` → `sr_queue.items[]`:

```json
{
  "id": "L2.S1.react-degradation::stop-condition-failures",
  "topic": "L2.S1.react-degradation",
  "question": "ReAct loops past 10 iterations tend to fail. Name two specific failure modes.",
  "answer_outline": "1) Goal drift — the model loses track of the original task as context grows. 2) Hallucinated tool calls — the model invents a tool that doesn't exist when it can't find a real one that fits.",
  "interval_days": 1,
  "ease": 2.5,
  "due": "2026-05-09",
  "history": [
    { "date": "2026-05-08", "rating": "good", "interval_after": 3 }
  ]
}
```

**Fields:**
- `id` — `<topic-id>::<short-slug>`. Stable.
- `topic` — points back into curriculum. `<layer>.<section>.<topic-slug>`.
- `question` — what the skill asks the learner.
- `answer_outline` — bullets, not prose. Skill uses this to grade the learner's response.
- `interval_days` — current interval. New items start at 1.
- `ease` — SM-2 ease factor. Starts at 2.5.
- `due` — date to ask next.
- `history` — append-only log: `{date, rating, interval_after}`.

---

## SM-2 lite scheduler

After the learner answers, the skill rates the response on a 4-level scale:

| Rating | Meaning |
|---|---|
| `again` | Wrong, or close to wrong. |
| `hard` | Got it but with hesitation or partial recall. |
| `good` | Correct, with reasonable speed. |
| `easy` | Instant, complete, no friction. |

### Update rules

```
if rating == "again":
    interval_days = 1
    ease = max(1.3, ease - 0.2)
elif rating == "hard":
    interval_days = max(1, round(interval_days * 1.2))
    ease = max(1.3, ease - 0.15)
elif rating == "good":
    interval_days = round(interval_days * ease)
    # ease unchanged
elif rating == "easy":
    interval_days = round(interval_days * ease * 1.3)
    ease = ease + 0.15

due = today + interval_days
history.append({ date: today, rating, interval_after: interval_days })
```

**Worked example.** New item, ease 2.5, interval 1.
- Day 1, rated `good` → interval = round(1 × 2.5) = 3, due day 4.
- Day 4, rated `hard` → interval = max(1, round(3 × 1.2)) = 4, ease = 2.35, due day 8.
- Day 8, rated `again` → interval = 1, ease = 2.15, due day 9.
- Day 9, rated `good` → interval = round(1 × 2.15) = 2, due day 11.
- Day 11, rated `good` → interval = round(2 × 2.15) = 4, due day 15.
- Day 15, rated `easy` → interval = round(4 × 2.15 × 1.3) = 11, ease = 2.30, due day 26.

---

## Daily review session

Triggered by `/quiz`, by an offer at session start ("SR queue has 4 items due — review first?"), or as part of an end-of-session pass.

1. Read `progress.json`. Filter `sr_queue.items` where `due <= today`.
2. Sort by `due` ascending (oldest first), then by `interval_days` ascending (shorter intervals first — they need more reps).
3. Cap at **15 items per session**. More than that and the learner zones out.
4. Ask each question. After their answer:
   - Reveal the `answer_outline`.
   - Rate the response (or ask "again / hard / good / easy?").
   - Apply scheduler rules. Write back to `progress.json`.
5. After the queue is empty (or capped), report: "5 reviewed: 3 good, 1 hard, 1 again. Next due 2026-05-11."

---

## Grading the learner's response

The skill is the grader. Rules:
- **Correct on the first attempt, no hedging** → `good` (or `easy` if it was instant and complete).
- **Correct after a hint or after partial recall** → `hard`.
- **Wrong on a key part** → `again`. Don't be charitable here — partial wrong is still wrong; better to over-review than to let a gap settle.
- **Right answer, wrong reasoning** → `again`. The reasoning is the thing being trained.

After grading, briefly explain *why* their answer landed where it did. SR is only useful if the learner sees their gap.

---

## Anti-patterns

- ❌ Asking the same SR item the same day it was generated. Min interval is 1 day.
- ❌ Rating everything `good` because the learner is "trying their best". Rate honestly; the schedule depends on it.
- ❌ Letting the queue exceed ~150 items. Above that, the daily review becomes punishing and gets skipped.
- ❌ Auto-deleting items after 5 successful reviews. Long-tail items still rot — keep them, just at long intervals.
- ❌ Not writing back to `progress.json` after a review. The schedule is useless if it doesn't persist.
- ❌ Adding SR items for trivial details. SR is for things that matter and are forgettable. "What's the third argument to Anthropic's `messages.create`?" is not SR-worthy.

---

## When SR isn't the right tool

Some material doesn't fit SR:
- **Procedural skills** (writing a ReAct loop): repetition through exercises, not flashcards.
- **Trade-off judgment** ("when do I pick LangGraph vs hand-rolled?"): live discussion / mock interview, not SR.
- **Architectural intuition**: cumulative across many lessons; SR catches pieces but misses the gestalt.

For these, fall back to mock interviews, design reviews, and capstone exercises per layer. SR is a complement, not a substitute.
