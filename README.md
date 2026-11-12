# sdlc-password-synthetic

Synthetic password-policy fixture for the AI SDLC Orchestrator sandbox runner.

## Local checks

```bash
uv sync --group dev
uv run --locked --group dev pytest -q
```

## Sandbox smoke test

`sandbox_pytest_smoke.py` uploads only the fixture's `pyproject.toml`, source
module, and tests to a temporary Vercel Sandbox. It installs pinned pytest while
network access is available, disables outbound network, runs pytest, then
destroys the sandbox.

Authenticate locally with `vercel link` and `vercel env pull .env.local` before
running `uv run python sandbox_pytest_smoke.py`. Keep `.env.local` out of Git.
The script loads local credentials for the SDK but does not upload that file or
pass those credentials into sandbox processes.
