"""Slack setup — idempotent channel creation.

On first run, creates one channel per agent + the war room. Re-running does nothing.
"""

import os
from slack_sdk.web import WebClient
from slack_sdk.errors import SlackApiError

from agents import ORG, WARROOM_CHANNEL


def setup_channels() -> dict[str, str]:
    """Create the agent channels + war room. Returns {channel_name: channel_id}."""
    token = os.getenv("SLACK_BOT_TOKEN")
    if not token:
        raise RuntimeError("SLACK_BOT_TOKEN not set in .env")
    client = WebClient(token=token)

    # Channels we want
    wanted = [a.channel for a in ORG] + [WARROOM_CHANNEL]
    existing = _list_all_channels(client)
    name_to_id: dict[str, str] = {c["name"]: c["id"] for c in existing}

    results: dict[str, str] = {}
    for name in wanted:
        if name in name_to_id:
            results[name] = name_to_id[name]
            print(f"  · #{name} (exists)")
            continue
        try:
            r = client.conversations_create(name=name, is_private=False)
            cid = r["channel"]["id"]
            results[name] = cid
            print(f"  + #{name} (created)")
        except SlackApiError as e:
            err = e.response.get("error", "unknown")
            if err == "name_taken":
                # Race — re-fetch
                latest = {c["name"]: c["id"] for c in _list_all_channels(client)}
                if name in latest:
                    results[name] = latest[name]
                    print(f"  · #{name} (race-recovered)")
            else:
                print(f"  ✗ #{name}: {err}")

    # Join all channels we created
    for name, cid in results.items():
        try:
            client.conversations_join(channel=cid)
        except SlackApiError:
            pass

    # Post a kickoff message in the war room so the founder knows it's alive
    if WARROOM_CHANNEL in results:
        try:
            client.chat_postMessage(
                channel=results[WARROOM_CHANNEL],
                text=(
                    "🟢 *Org Bridge online.*\n"
                    "Each agent has its own channel — DM them there. "
                    "Status updates land here in the war room. "
                    "Talk to *Devika (Chief of Staff)* in #org-chief to kick things off."
                ),
            )
        except SlackApiError:
            pass

    return results


def _list_all_channels(client: WebClient) -> list[dict]:
    out: list[dict] = []
    cursor = None
    while True:
        r = client.conversations_list(
            exclude_archived=True,
            types="public_channel,private_channel",
            limit=1000,
            cursor=cursor,
        )
        out.extend(r.get("channels", []))
        cursor = r.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
    return out


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    print("Setting up Slack channels...")
    setup_channels()
    print("Done.")
