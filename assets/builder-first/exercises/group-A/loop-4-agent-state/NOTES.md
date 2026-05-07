# Loop 4 — Notes

*Fill in as you go. Three short paragraphs each.*

## Concept

What this loop teaches in your own words. The trio of memories (short / working / long-term) and what each one is for. Why agent state is *just files and dicts*, and why that's a more useful mental model than thinking of agents as black boxes.

## The break

What was missing in the starter and what each missing piece would have cost a real agent. Specifically:
- What happens to a chatbot without a `recall` tool?
- What does a long conversation look like without compaction (token cost, context-window failure)?
- What does removing a tool mid-session reveal about how the model treats its own toolbox?
- What did hand-editing `memory.json` feel like — was it surprising that it worked? Why or why not?

## The fix

What changes resolved each. Specifically:
- When you reach for **working memory** vs **long-term memory** in a real agent design (one paragraph).
- What you found about compaction quality — did your summary prompt lose any facts the agent later needed? What would you tighten?
- The graceful-failure-vs-hallucination outcome from `/tools remove calculator`. If hallucination — what would you do about it in a real agent? (Tee up Loop 7b's anti-pattern beat.)
- One sentence on why "agent state is just files" matters for production debugging — you can read state, edit state, ship state.
