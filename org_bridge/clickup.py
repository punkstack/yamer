"""ClickUp helper — thin wrapper over the REST API.

Uses the personal API key from .env. Idempotent task creation (searches before creating).
"""

import os
import httpx
from dataclasses import dataclass

BASE = "https://api.clickup.com/api/v2"


def _headers() -> dict:
    api_key = os.getenv("CLICKUP_API_KEY", "")
    if not api_key:
        raise RuntimeError("CLICKUP_API_KEY not set in .env")
    return {"Authorization": api_key, "Content-Type": "application/json"}


def _list_id() -> str:
    lid = os.getenv("CLICKUP_LIST_ID", "")
    if not lid:
        raise RuntimeError("CLICKUP_LIST_ID not set in .env")
    return lid


@dataclass
class Task:
    id: str
    name: str
    status: str
    url: str


async def search_tasks(query: str) -> list[Task]:
    """Search tasks in the configured list by name substring."""
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.get(f"{BASE}/list/{_list_id()}/task", headers=_headers())
        r.raise_for_status()
        tasks = r.json().get("tasks", [])
        q = query.lower()
        return [
            Task(id=t["id"], name=t["name"], status=t.get("status", {}).get("status", ""), url=t.get("url", ""))
            for t in tasks
            if q in t.get("name", "").lower()
        ]


async def create_task(
    name: str,
    description: str,
    status: str = "Spec",
    tags: list[str] | None = None,
    *,
    dedupe: bool = True,
) -> Task:
    """Create a task. If dedupe=True, returns the existing task instead of duplicating."""
    if dedupe:
        existing = await search_tasks(name)
        exact = [t for t in existing if t.name.strip().lower() == name.strip().lower()]
        if exact:
            return exact[0]

    payload = {
        "name": name,
        "description": description,
        "status": status,
        "tags": tags or [],
    }
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.post(f"{BASE}/list/{_list_id()}/task", headers=_headers(), json=payload)
        r.raise_for_status()
        t = r.json()
        return Task(id=t["id"], name=t["name"], status=t.get("status", {}).get("status", ""), url=t.get("url", ""))


async def update_status(task_id: str, status: str) -> None:
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.put(f"{BASE}/task/{task_id}", headers=_headers(), json={"status": status})
        r.raise_for_status()


async def list_open() -> list[Task]:
    """All tasks in the configured list that aren't Done."""
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.get(
            f"{BASE}/list/{_list_id()}/task",
            headers=_headers(),
            params={"include_closed": "false"},
        )
        r.raise_for_status()
        return [
            Task(id=t["id"], name=t["name"], status=t.get("status", {}).get("status", ""), url=t.get("url", ""))
            for t in r.json().get("tasks", [])
        ]
