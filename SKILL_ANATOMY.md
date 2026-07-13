# Skill anatomy

| Shared component | Location |
|---|---|
| Router and onboarding | `SKILL.md` |
| Foundations curriculum | `references/curriculum.md` |
| Top-down practical path | `references/builder-first.md` and `assets/builder-first/` |
| Exercises | `references/exercise-bank.md` and `assets/exercise-templates/` |
| Incidents and teaching modes | `references/incidents.md`, `references/theory-modes.md` |
| Session and review | `references/session-control.md`, `references/spaced-repetition.md` |
| Anti-patterns and host portability | `references/anti-patterns-with-examples.md`, `references/host-adapters.md` |
| Learner state and verification | `assets/progress-template.json`, `tests/` |

Every new course feature belongs in one of these layers. Keep `SKILL.md` as the router and
lazy-load the detailed reference rather than duplicating it there.
