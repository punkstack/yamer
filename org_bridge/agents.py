"""Agent registry — the org, with Slack identities.

Each agent has:
- a Slack display name + icon (how it shows up in messages)
- a channel slug (the dedicated channel where the founder talks to them)
- a path to its system prompt (the same .md file Claude Code reads)
- which Claude model class to use
- whether it can be invoked directly by the founder (true for all except auditor)
"""

from pathlib import Path
from dataclasses import dataclass

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
