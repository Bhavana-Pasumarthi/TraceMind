# Simulator

Not yet implemented — this is Phase 3 (simulated services) and Phase 4/5
(log/metric/trace generators, incident generator with failure scenarios).

Planned layout:
- `services/` — lightweight FastAPI stand-ins for user/order/payment/inventory services
- `generators/` — log/metric/trace generation logic
- `failure_scenarios/` — one file per failure scenario (trigger, expected evidence, ground truth)
- `data/` — scratch space used while generating, before writing to Postgres
