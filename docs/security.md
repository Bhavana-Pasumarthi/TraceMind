# Security

## As of Phase 1

- Secrets are read from environment variables via `.env` (never
  committed — see `.gitignore`); `.env.example` documents required
  variables with placeholder values only.
- CORS is wide open (`allow_origins=["*"]`) in `environment=development`
  only, and explicitly empty otherwise — this will need a real allowlist
  before Phase 15 (docs + polish) if this is ever exposed beyond
  localhost.
- No authentication yet — there is nothing to authenticate to (no
  incidents, no user-facing actions beyond a health check).
- No LLM calls yet, so prompt-injection defenses (documented in
  `docs/agent-design.md` once written) don't apply yet.

## Ongoing commitments (enforced starting the phases noted)

- Pydantic validates every API input (Phase 2 onward, as real endpoints
  are added).
- No arbitrary shell execution by the AI, ever — remediation actions are
  a fixed catalog (Phase 11), and the Validation Agent runs them in a
  Docker sandbox, not on the host (Phase 12).
- Retrieved documents (runbooks, historical incidents) are treated as
  data, never as instructions the LLM should follow (Phase 8-9).
