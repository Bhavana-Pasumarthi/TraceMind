"""
Deterministic incident generator — STUB (Phase 5).

Once implemented, running:

    python scripts/generate_incidents.py --scenario db_pool_exhaustion --seed 42

will deterministically generate normal + injected-failure operational data
(logs, metrics, traces, deployments) and write it into Postgres, plus create
the corresponding `incidents` row. The same seed + scenario must always
produce identical data (required for reproducible demos and evaluation).

Not implemented yet — Phases 1-4 (schema, simulated services, generators)
must land first.
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="TraceMind incident generator (stub)")
    parser.add_argument("--scenario", default="none", help="Failure scenario ID, or 'none' for normal data only")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    raise NotImplementedError(
        f"generate_incidents.py is a Phase 5 stub. "
        f"Requested scenario={args.scenario!r} seed={args.seed} — not yet implemented."
    )


if __name__ == "__main__":
    main()
