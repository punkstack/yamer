"""Claude loop — invoke an agent and stream its response back to the caller.

Two runtimes:
  - "code"  → shells out to `claude -p` (Claude Code, Max subscription billing)
  - "api"   → uses the Claude Agent SDK (API billing)

Default is "code" because the user is on Claude Max.
"""

import asyncio
import json
import os
from typing import AsyncIterator

from agents import Agent, ORG_ROOT


CLAUDE_RUNTIME = os.getenv("CLAUDE_RUNTIME", "code")

# Claude Code accepts short aliases; they auto-resolve to the latest version
# of that family, so we don't have to chase version numbers.
MODEL_ALIAS = {"haiku": "haiku", "sonnet": "sonnet", "opus": "opus"}


# -------------------------------------------------------------------
# Runtime 1: Claude Code headless (preferred — uses Max subscription)
# -------------------------------------------------------------------

async def run_via_code(agent: Agent, prompt: str) -> AsyncIterator[str]:
    """Stream output from `claude -p` running in the org root directory."""
    system_prompt = agent.load_prompt()
    full_prompt = (
        f"You are {agent.display_name}.\n\n"
        f"{system_prompt}\n\n"
        f"---\n{prompt}"
    )
    model = MODEL_ALIAS.get(agent.model, "sonnet")

    cmd = [
        "claude", "-p", full_prompt,
        "--model", model,
        "--output-format", "stream-json",
    ]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=str(ORG_ROOT),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    assert proc.stdout is not None
    async for line in proc.stdout:
        try:
            obj = json.loads(line.decode().strip() or "{}")
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "content_block_delta":
            delta = obj.get("delta", {}).get("text", "")
            if delta:
                yield delta
        elif obj.get("type") == "message_delta" and obj.get("delta", {}).get("stop_reason"):
            break

    await proc.wait()
    if proc.returncode != 0 and proc.stderr is not None:
        err = (await proc.stderr.read()).decode()
        if err.strip():
            yield f"\n_[runtime error: {err[:500]}]_"


# -------------------------------------------------------------------
# Runtime 2: Claude Agent SDK (API billing)
# -------------------------------------------------------------------

async def run_via_sdk(agent: Agent, prompt: str) -> AsyncIterator[str]:
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

    options = ClaudeAgentOptions(
        model=MODEL_ALIAS.get(agent.model, "sonnet"),
        system_prompt=agent.load_prompt(),
        cwd=str(ORG_ROOT),
        allowed_tools=["Read", "Write", "Edit", "Bash", "Grep", "Glob", "WebSearch", "WebFetch"],
        setting_sources=["project"],
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)
        async for msg in client.receive_response():
            text = getattr(msg, "text", None) or str(msg)
            if text:
                yield text


# -------------------------------------------------------------------
# Public entry point
# -------------------------------------------------------------------

async def run_agent(agent: Agent, prompt: str) -> AsyncIterator[str]:
    """Run an agent for one turn. Streams text deltas.

    `prompt` is the full message to send. The bridge is responsible for
    including any chat history in `prompt` if continuity is needed.
    """
    runtime = (CLAUDE_RUNTIME or "code").lower()
    runner = run_via_code if runtime == "code" else run_via_sdk
    async for chunk in runner(agent, prompt):
        yield chunk
