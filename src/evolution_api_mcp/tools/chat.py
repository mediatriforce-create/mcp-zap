"""Chat management tools for Evolution API v1.8.x."""

from typing import Any

from evolution_api_mcp.client import get_client


async def find_contact(instance_name: str, name: str) -> dict:
    """Search for a WhatsApp contact by name and return their JID (phone number).

    Args:
        instance_name: Name of the connected instance
        name: Full or partial name to search (case-insensitive)
    """
    chats = await get_client().get(f"chat/findChats/{instance_name}")
    if not isinstance(chats, list):
        return {"error": "Could not fetch chats"}

    name_lower = name.lower()
    matches = []
    for chat in chats:
        push_name = (chat.get("name") or chat.get("pushName") or "").lower()
        jid = chat.get("id", "")
        if name_lower in push_name:
            matches.append({"jid": jid, "name": chat.get("name") or chat.get("pushName"), "last_message": chat.get("lastMsgTimestamp")})

    if not matches:
        # fallback: search in recent messages pushName
        return {"found": False, "message": f"Nenhum contato encontrado com o nome '{name}'"}

    return {"found": True, "contacts": matches}


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


async def download_media(
    instance_name: str,
    message_id: str,
    remote_jid: str,
    from_me: bool = False,
) -> dict:
    """Download media (image, video, audio, document) from a received WhatsApp message.
    Returns base64-encoded content and mimetype.

    Args:
        instance_name: Name of the connected instance
        message_id: ID of the message containing the media
        remote_jid: Chat JID the message belongs to (e.g. "5511999999999@s.whatsapp.net")
        from_me: Whether the message was sent by you (default False)
    """
    return await get_client().post(
        f"chat/getBase64FromMediaMessage/{instance_name}",
        json_data={
            "message": {
                "key": {
                    "id": message_id,
                    "remoteJid": remote_jid,
                    "fromMe": from_me,
                }
            },
            "convertToMp4": False,
        },
    )


async def check_number(instance_name: str, number: str) -> dict:
    """Check if a phone number exists on WhatsApp before sending a message.

    Args:
        instance_name: Name of the connected instance
        number: Phone number with country code (e.g. "5511999999999")
    """
    return await get_client().get(
        f"chat/whatsappNumbers/{instance_name}",
        params={"numbers": number},
    )


async def set_presence(
    instance_name: str,
    number: str,
    presence: str = "composing",
    delay: int = 2000,
) -> dict:
    """Set presence status in a chat (e.g. show 'typing...' before sending a message).

    Args:
        instance_name: Name of the connected instance
        number: Recipient phone number with country code (e.g. "5511999999999")
        presence: Presence type. Values: composing (typing), recording (audio), paused, available, unavailable
        delay: Duration in milliseconds to show the presence (default 2000)
    """
    return await get_client().post(
        f"chat/sendPresence/{instance_name}",
        json_data={
            "number": number,
            "options": {"presence": presence, "delay": delay},
        },
    )


async def delete_message(
    instance_name: str,
    remote_jid: str,
    message_id: str,
    from_me: bool = True,
) -> dict:
    """Delete a sent WhatsApp message (delete for everyone).

    Args:
        instance_name: Name of the connected instance
        remote_jid: Chat JID (e.g. "5511999999999@s.whatsapp.net")
        message_id: ID of the message to delete
        from_me: Whether the message was sent by you (default True)
    """
    return await get_client().delete(
        f"chat/deleteMessageForEveryone/{instance_name}/{remote_jid}/{message_id}/{str(from_me).lower()}",
    )


async def mark_chat_unread(
    instance_name: str,
    remote_jid: str,
    last_message_id: str,
    from_me: bool = False,
) -> dict:
    """Mark a chat as unread.

    Args:
        instance_name: Name of the connected instance
        remote_jid: Chat JID (e.g. "5511999999999@s.whatsapp.net")
        last_message_id: ID of the last message in the chat
        from_me: Whether the last message was sent by you
    """
    return await get_client().put(
        f"chat/markChatUnread/{instance_name}",
        json_data={
            "lastMessage": {
                "key": {
                    "remoteJid": remote_jid,
                    "id": last_message_id,
                    "fromMe": from_me,
                }
            }
        },
    )


async def list_contacts(instance_name: str) -> dict:
    """List all contacts saved in the WhatsApp account phonebook.

    Args:
        instance_name: Name of the connected instance
    """
    return await get_client().get(f"chat/findContacts/{instance_name}")


async def get_profile(instance_name: str, number: str) -> dict:
    """Get WhatsApp profile info (name, picture URL, status) of a contact.

    Args:
        instance_name: Name of the connected instance
        number: Phone number with country code (e.g. "5511999999999")
    """
    return await get_client().get(
        f"chat/fetchProfile/{instance_name}",
        params={"number": number},
    )
