"""Group management tools for Evolution API v1.8.x."""

from typing import Any

from evolution_api_mcp.client import get_client


async def create_group(
    instance_name: str,
    subject: str,
    participants: list[str],
    description: str = "",
) -> dict:
    """Create a new WhatsApp group.

    Args:
        instance_name: Name of the connected instance
        subject: Group name/title
        participants: List of phone numbers to add (e.g. ["5511999999999", "5511888888888"])
        description: Group description (optional)
    """
    body: dict[str, Any] = {
        "subject": subject,
        "participants": participants,
    }
    if description:
        body["description"] = description
    return await get_client().post(
        f"group/create/{instance_name}", json_data=body
    )


async def add_participants(
    instance_name: str,
    group_jid: str,
    participants: list[str],
) -> dict:
    """Add participants to a WhatsApp group.

    Args:
        instance_name: Name of the connected instance
        group_jid: Group JID (e.g. "120363000000000000@g.us")
        participants: List of phone numbers to add (e.g. ["5511999999999"])
    """
    return await get_client().put(
        f"group/updateParticipant/{instance_name}",
        json_data={
            "groupJid": group_jid,
            "action": "add",
            "participants": participants,
        },
    )


async def remove_participants(
    instance_name: str,
    group_jid: str,
    participants: list[str],
) -> dict:
    """Remove participants from a WhatsApp group.

    Args:
        instance_name: Name of the connected instance
        group_jid: Group JID (e.g. "120363000000000000@g.us")
        participants: List of phone numbers to remove (e.g. ["5511999999999"])
    """
    return await get_client().put(
        f"group/updateParticipant/{instance_name}",
        json_data={
            "groupJid": group_jid,
            "action": "remove",
            "participants": participants,
        },
    )


async def update_group_name(
    instance_name: str,
    group_jid: str,
    subject: str,
) -> dict:
    """Update the name/subject of a WhatsApp group.

    Args:
        instance_name: Name of the connected instance
        group_jid: Group JID (e.g. "120363000000000000@g.us")
        subject: New group name
    """
    return await get_client().put(
        f"group/updateGroupSubject/{instance_name}",
        json_data={"groupJid": group_jid, "subject": subject},
    )


async def list_groups(instance_name: str) -> dict:
    """List all WhatsApp groups the connected account is part of.

    Args:
        instance_name: Name of the connected instance
    """
    return await get_client().get(
        f"group/fetchAllGroups/{instance_name}",
        params={"getParticipants": "false"},
    )


async def get_group_info(instance_name: str, group_jid: str) -> dict:
    """Get detailed info about a WhatsApp group including participants.

    Args:
        instance_name: Name of the connected instance
        group_jid: Group JID (e.g. "120363000000000000@g.us")
    """
    return await get_client().get(
        f"group/findGroupInfos/{instance_name}",
        params={"groupJid": group_jid},
    )


async def leave_group(instance_name: str, group_jid: str) -> dict:
    """Leave a WhatsApp group.

    Args:
        instance_name: Name of the connected instance
        group_jid: Group JID (e.g. "120363000000000000@g.us")
    """
    return await get_client().delete(
        f"group/leaveGroup/{instance_name}?groupJid={group_jid}",
    )
