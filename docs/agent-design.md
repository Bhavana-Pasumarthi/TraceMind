# Agent Design

Not yet implemented — agents arrive in Phase 9, after the deterministic
system (Phases 1-8) works end-to-end without any LLM involvement.

Planned content once implemented:
- Full responsibility table for Orchestrator, Evidence Collection,
  Evidence Correlation, Root Cause Analysis, Remediation, Validation
  (see `docs/architecture.md` for the current graph shape).
- Exact tool signatures each stage can call (typed Pydantic in/out).
- How FACT / EVIDENCE / HYPOTHESIS categories are enforced in code,
  not just in prompts.
- Prompt-injection defenses: retrieved runbook/historical-incident text
  is always passed as data in a structured field, never concatenated
  into an instruction-bearing part of the prompt.
