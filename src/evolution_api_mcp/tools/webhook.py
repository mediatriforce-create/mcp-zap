"""Webhook management tools for Evolution API v1.8.x."""

from typing import Any

from evolution_api_mcp.client import get_client


async def set_webhook(
    instance_name: str,
    url: str,
    events: list[str] | None = None,
    enabled: bool = True,
    webhook_by_events: bool = False,
    webhook_base64: bool = False,
) -> dict:
    """Configure a webhook URL to receive real-time WhatsApp events (incoming messages, etc).

    Args:
        instance_name: Name of the connected instance
        url: Public URL that will receive POST requests with event data
        events: List of events to subscribe to. Default: all main events.
            Options: MESSAGES_UPSERT, MESSAGES_UPDATE, MESSAGES_DELETE,
            SEND_MESSAGE, CONTACTS_UPSERT, CONTACTS_UPDATE,
            PRESENCE_UPDATE, CHATS_UPSERT, CHATS_UPDATE, CHATS_DELETE,
            GROUPS_UPSERT, GROUP_UPDATE, GROUP_PARTICIPANTS_UPDATE,
            CONNECTION_UPDATE, CALL, NEW_JWT_TOKEN
        enabled: Enable or disable the webhook
        webhook_by_events: If True, appends event name to URL path (e.g. url/MESSAGES_UPSERT)
        webhook_base64: If True, sends media as base64 in webhook payload
    """
    if events is None:
        events = [
            "MESSAGES_UPSERT",
            "MESSAGES_UPDATE",
            "MESSAGES_DELETE",
            "SEND_MESSAGE",
            "CONNECTION_UPDATE",
        ]
    body: dict[str, Any] = {
        "enabled": enabled,
        "url": url,
        "webhookByEvents": webhook_by_events,
        "webhookBase64": webhook_base64,
        "events": events,
    }
    return await get_client().post(
        f"webhook/set/{instance_name}", json_data=body
    )


async def get_webhook(instance_name: str) -> dict:
    """Get the current webhook configuration for an instance.

    Args:
        instance_name: Name of the connected instance
    """
    return await get_client().get(f"webhook/find/{instance_name}")


async def disable_webhook(instance_name: str) -> dict:
    """Disable the webhook for an instance (stops receiving real-time events).

    Args:
        instance_name: Name of the connected instance
    """
    current = await get_client().get(f"webhook/find/{instance_name}")
    url = current.get("url", "")
    events = current.get("events", [])
    body: dict[str, Any] = {
        "enabled": False,
        "url": url,
        "events": events,
    }
    return await get_client().post(
        f"webhook/set/{instance_name}", json_data=body
    )
