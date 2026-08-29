"""Diagnostic-only Omnigent guardrail policies — log, never gate.

Step 1 of designing a real enforcement gate (see
dev-infrastructure/specs/omnigent-setup.md and the 2026-08-29 session note):
before writing a policy that DENYs/ASKs on a missing `requirements-gather`
skill-load, we need the REAL shape of a Skill-tool `tool_call` event as
Omnigent's policy engine actually sees it — inferred so far (Polly's brain
runs the `claude-sdk` harness, which ships a native `Skill` tool; the
"Launching skill: polly:X" text observed in live transcripts does not
appear anywhere in the installed `omnigent` package's source, so it likely
renders from that native tool, not from Omnigent itself) but not yet
directly confirmed. This module only logs; it always ALLOWs, so it is safe
to attach to any live deployment.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def log_tool_call_events(log_path: str = "~/omnigent-policy-debug.log") -> Any:
    """Factory: returns a policy callable that logs every event and always ALLOWs.

    :param log_path: Where to append one JSON line per policy-engine event.
        Expanded with ``Path.expanduser()`` so ``~`` works from YAML.
    :returns: A one-arg callable suitable for a FunctionPolicy (see
        ``omnigent.policies.function.resolve_function_policy`` — a spec with
        non-None ``arguments`` treats this factory's return value, not the
        factory itself, as the evaluator).
    """
    resolved_path = Path(log_path).expanduser()

    def _evaluator(event: dict[str, Any]) -> dict[str, str]:
        """Append `event` as one JSON line, then unconditionally ALLOW.

        Never raises — a logging failure must not be able to block or deny
        a real dispatch just because this diagnostic policy is attached.
        """
        try:
            resolved_path.parent.mkdir(parents=True, exist_ok=True)
            record = {
                "type": event.get("type"),
                "target": event.get("target"),
                "data": event.get("data"),
                "request_data": event.get("request_data"),
            }
            with resolved_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, default=str) + "\n")
        except OSError:
            pass
        return {"result": "ALLOW"}

    return _evaluator
