"""Chat management tools for Evolution API v1.8.x."""

from typing import Any

from evolution_api_mcp.client import get_client


async def find_chats(instance_name: str) -> dict:
    """List all chats/conversations of the connected WhatsApp account.

    Args:
        instance_name: Name of the connected instance
    """
    return await get_client().get(f"chat/findChats/{instance_name}")


async def find_messages(
    instance_name: str,
    remote_jid: str,
    limit: int = 20,
    page: int = 1,
) -> dict:
    """Find messages from a specific chat.

    Args:
        instance_name: Name of the connected instance
        remote_jid: Chat JID (e.g. "5511999999999@s.whatsapp.net" for individual, "groupid@g.us" for group)
        limit: Number of messages to return (default 20)
        page: Page number for pagination (default 1)
    """
    body: dict[str, Any] = {
        "where": {"key": {"remoteJid": remote_jid}},
        "limit": limit,
        "page": page,
    }
    return await get_client().post(
        f"chat/findMessages/{instance_name}", json_data=body
    )


async def archive_chat(
    instance_name: str,
    chat_jid: str,
    last_message_id: str,
    from_me: bool = False,
    archive: bool = True,
) -> dict:
    """Archive or unarchive a chat.

    Args:
        instance_name: Name of the connected instance
        chat_jid: Chat JID (e.g. "5511999999999@s.whatsapp.net")
        last_message_id: ID of the last message in the chat
        from_me: Whether the last message was sent by you
        archive: True to archive, False to unarchive
    """
    return await get_client().put(
        f"chat/archiveChat/{instance_name}",
        json_data={
            "lastMessage": {
                "key": {
                    "remoteJid": chat_jid,
                    "id": last_message_id,
                    "fromMe": from_me,
                }
            },
            "archive": archive,
        },
    )


async def mark_message_as_read(
    instance_name: str,
    remote_jid: str,
    message_id: str,
    from_me: bool = False,
) -> dict:
    """Mark a message as read.

    Args:
        instance_name: Name of the connected instance
        remote_jid: Chat JID (e.g. "5511999999999@s.whatsapp.net")
        message_id: ID of the message to mark as read
        from_me: Whether the message was sent by you
    """
    return await get_client().put(
        f"chat/markMessageAsRead/{instance_name}",
        json_data={
            "read_messages": [
                {
                    "remoteJid": remote_jid,
                    "fromMe": from_me,
                    "id": message_id,
                }
            ]
        },
    )
