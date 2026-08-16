# Evaluation

Not yet implemented — the benchmark harness and rule-based baseline are
built in Phase 13, after remediation and validation exist to evaluate.

Planned metrics: root-cause accuracy (top-1 and top-K), evidence
retrieval recall, evidence grounding, remediation validation success
rate, and per-stage latency. Ground truth root causes are stored
separately from anything the agent pipeline can query — see the Phase 0
plan (`tracemind-architecture-plan.md`, §10) for how that separation is
enforced. Results reported here will be actual measured numbers from
running the benchmark, not estimates.
