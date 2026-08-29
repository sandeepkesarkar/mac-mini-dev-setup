"""Locally-authored Omnigent guardrail policies for this deployment.

Deliberately named `polly_policies`, NOT `omnigent` — this repo also has a
top-level `omnigent/` directory (Polly's config + poller), and adding that
to PYTHONPATH would shadow the real installed `omnigent` pip package,
breaking the server for every session on this machine. This package's name
has no collision risk with anything already on the interpreter's path.
"""
