"""Agent registry — the org, with Slack identities.

Each agent has:
- a Slack display name + icon (how it shows up in messages)
- a channel slug (the dedicated channel where the founder talks to them)
- a path to its system prompt (the same .md file Claude Code reads)
- which Claude model class to use
- whether it can be invoked directly by the founder (true for all except auditor)
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass

log = logging.getLogger("org-bridge.agents")

ORG_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ORG_ROOT / ".claude" / "agents"


@dataclass
class Agent:
    key: str                # internal id (matches subagent name)
    persona: str            # human name shown in Slack
    role: str               # short role label
    icon: str               # emoji shown next to messages
    channel: str            # channel slug (without #)
    model: str              # "haiku" | "sonnet" | "opus"
    prompt_file: str        # which .md file in .claude/agents/
    invokable_by_founder: bool = True

    @property
    def display_name(self) -> str:
        return f"{self.persona} ({self.role})"

    def load_prompt(self) -> str:
        path = AGENTS_DIR / self.prompt_file
        if not path.exists():
            return f"You are {self.display_name}. Prompt file missing — refuse to act."
        return path.read_text()


# The org — order matters for setup script (Chief of Staff first).
ORG: list[Agent] = [
    Agent(
        key="chief",
        persona="Devika",
        role="Chief of Staff",
        icon=":busts_in_silhouette:",
        channel="org-chief",
        model="opus",
        prompt_file="../../CLAUDE.md",        # the orchestrator prompt
        invokable_by_founder=True,
    ),
    Agent(
        key="spm",
        persona="Sarah",
        role="Senior PM",
        icon=":memo:",
        channel="org-sarah-spm",
        model="sonnet",
        prompt_file="spm.md",
    ),
    Agent(
        key="pm",
        persona="Priya",
        role="Project Manager",
        icon=":clipboard:",
        channel="org-priya-pm",
        model="sonnet",
        prompt_file="pm.md",
    ),
    Agent(
        key="backend",
        persona="Raj",
        role="Staff Backend",
        icon=":electric_plug:",
        channel="org-raj-backend",
        model="sonnet",
        prompt_file="staff-backend.md",
    ),
    Agent(
        key="frontend",
        persona="Mia",
        role="Staff Frontend",
        icon=":art:",
        channel="org-mia-frontend",
        model="sonnet",
        prompt_file="staff-frontend.md",
    ),
    Agent(
        key="devops",
        persona="Karthik",
        role="DevOps / SRE",
        icon=":gear:",
        channel="org-karthik-devops",
        model="sonnet",
        prompt_file="devops.md",
    ),
    Agent(
        key="gitops",
        persona="Ravi",
        role="GitOps",
        icon=":twisted_rightwards_arrows:",
        channel="org-ravi-gitops",
        model="sonnet",
        prompt_file="gitops.md",
    ),
    Agent(
        key="innovator",
        persona="Alex",
        role="Principal / Contrarian",
        icon=":dart:",
        channel="org-alex-innovator",
        model="opus",
        prompt_file="innovator.md",
    ),
    Agent(
        key="gtm",
        persona="Neha",
        role="Product Marketing",
        icon=":loudspeaker:",
        channel="org-neha-gtm",
        model="haiku",
        prompt_file="gtm.md",
    ),
    Agent(
        key="qa",
        persona="Vikram",
        role="QA / Risk",
        icon=":mag:",
        channel="org-vikram-qa",
        model="sonnet",
        prompt_file="qa.md",
    ),
    Agent(
        key="auditor",
        persona="The Auditor",
        role="Stage Gate",
        icon=":lock:",
        channel="org-auditor",
        model="sonnet",
        prompt_file="auditor.md",
        invokable_by_founder=False,        # only invoked by Chief of Staff after stages
    ),
    Agent(
        key="platform",
        persona="Arjun",
        role="Platform Engineer",
        icon=":wrench:",
        channel="org-arjun-platform",
        model="sonnet",
        prompt_file="platform.md",
    ),
]


# Lookup helpers
BY_KEY = {a.key: a for a in ORG}
BY_CHANNEL = {a.channel: a for a in ORG}


def agent_for_channel(channel_name: str) -> Agent | None:
    """Given a Slack channel name (without leading #), return the agent that owns it."""
    return BY_CHANNEL.get(channel_name.lstrip("#"))


def all_channels() -> list[str]:
    return [a.channel for a in ORG]


# The shared war-room channel — agents drop status, founder watches the org work.
WARROOM_CHANNEL = "org-warroom"

# The pulse transparency channel — bot-only, 10-min snapshots.
PULSE_CHANNEL = "org-pulse"


# -------------------------------------------------------------------
# Agent status helpers — write to memory/agent-status.json
# -------------------------------------------------------------------

def _status_file(root: Path) -> Path:
    return root / "memory" / "agent-status.json"


def write_agent_status(root: Path, agent_key: str, state: str, task: str = "") -> None:
    """Write or update a single agent's status in memory/agent-status.json.

    state: "active" | "idle" | "stalled"
    task:  short description of current work (empty string when idle)
    Called by main.py at dispatch entry and on completion/error.
    """
    status_file = _status_file(root)
    status_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        existing: dict = json.loads(status_file.read_text()) if status_file.exists() else {}
    except (json.JSONDecodeError, OSError):
        existing = {}

    now = datetime.now(timezone.utc).isoformat()
    entry = existing.get(agent_key, {})

    if state == "active":
        # Preserve the original start_ts if already active (re-entry guard)
        updated = {
            "state": "active",
            "task": task,
            "start_ts": entry.get("start_ts", now) if entry.get("state") == "active" else now,
            "last_update_ts": now,
            "last_artifact": entry.get("last_artifact"),
        }
    elif state == "idle":
        updated = {
            "state": "idle",
            "task": "",
            "start_ts": None,
            "last_update_ts": now,
            "last_artifact": entry.get("last_artifact"),
        }
    else:  # stalled — set by pulse, not by dispatch
        updated = {**entry, "state": "stalled", "last_update_ts": now}

    existing[agent_key] = updated

    try:
        status_file.write_text(json.dumps(existing, indent=2))
    except OSError:
        log.exception("write_agent_status: failed to write %s", status_file)


def record_artifact(root: Path, agent_key: str, slug: str, doc_type: str) -> None:
    """Update last_artifact for an agent after a successful publish."""
    status_file = _status_file(root)
    try:
        existing: dict = json.loads(status_file.read_text()) if status_file.exists() else {}
    except (json.JSONDecodeError, OSError):
        existing = {}

    entry = existing.get(agent_key, {})
    existing[agent_key] = {
        **entry,
        "last_artifact": f"{slug}-{doc_type}",
        "last_artifact_ts": datetime.now(timezone.utc).isoformat(),
    }
    try:
        status_file.write_text(json.dumps(existing, indent=2))
    except OSError:
        log.exception("record_artifact: failed to write %s", status_file)
