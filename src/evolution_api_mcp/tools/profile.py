"""Profile and contact management tools for Evolution API v1.8.x."""

from typing import Any

from evolution_api_mcp.client import get_client


async def update_profile_name(instance_name: str, name: str) -> dict:
    """Update the display name of your WhatsApp account.

    Args:
        instance_name: Name of the connected instance
        name: New display name to set on your WhatsApp profile
    """
    return await get_client().post(
        f"chat/updateProfileName/{instance_name}",
        json_data={"name": name},
    )


async def update_profile_picture(instance_name: str, image: str) -> dict:
    """Update your WhatsApp profile picture.

    Args:
        instance_name: Name of the connected instance
        image: URL or base64-encoded image (JPG/PNG recommended, square crop)
    """
    return await get_client().put(
        f"chat/updateProfilePicture/{instance_name}",
        json_data={"picture": image},
    )


async def update_profile_status(instance_name: str, status: str) -> dict:
    """Update your WhatsApp profile status text (bio).

    Args:
        instance_name: Name of the connected instance
        status: Status text to display on your profile
    """
    return await get_client().post(
        f"chat/updateProfileStatus/{instance_name}",
        json_data={"status": status},
    )


async def block_contact(instance_name: str, number: str) -> dict:
    """Block a WhatsApp contact.

    Args:
        instance_name: Name of the connected instance
        number: Phone number to block with country code (e.g. "5511999999999")
    """
    return await get_client().post(
        f"chat/updateBlockStatus/{instance_name}",
        json_data={"number": number, "status": "block"},
    )


async def unblock_contact(instance_name: str, number: str) -> dict:
    """Unblock a previously blocked WhatsApp contact.

    Args:
        instance_name: Name of the connected instance
        number: Phone number to unblock with country code (e.g. "5511999999999")
    """
    return await get_client().post(
        f"chat/updateBlockStatus/{instance_name}",
        json_data={"number": number, "status": "unblock"},
    )


async def send_status(
    instance_name: str,
    content: str,
    status_type: str = "text",
    background_color: str = "#000000",
    font: int = 1,
    caption: str = "",
) -> dict:
    """Send a WhatsApp status update (story visible to all contacts).

    Args:
        instance_name: Name of the connected instance
        content: Text content or URL/base64 for image/video status
        status_type: Type of status. Values: text, image, video, audio
        background_color: Background color for text status (hex, e.g. "#FF5733")
        font: Font style for text status (1-5)
        caption: Caption text for image/video status
    """
    body: dict[str, Any] = {
        "type": status_type,
        "content": content,
    }
    if status_type == "text":
        body["backgroundColor"] = background_color
        body["font"] = font
    elif caption:
        body["caption"] = caption

    return await get_client().post(
        f"message/sendStatus/{instance_name}", json_data=body
    )


async def search_messages(
    instance_name: str,
    query: str,
    remote_jid: str | None = None,
    limit: int = 20,
) -> dict:
    """Search messages by keyword across chats or within a specific chat.

    Args:
        instance_name: Name of the connected instance
        query: Text to search for in message content
        remote_jid: Optional chat JID to restrict search (e.g. "5511999999999@s.whatsapp.net")
        limit: Maximum number of results to return (default 20)
    """
    where: dict[str, Any] = {
        "message": {"conversation": {"contains": query}}
    }
    if remote_jid:
        where["key"] = {"remoteJid": remote_jid}

    return await get_client().post(
        f"chat/findMessages/{instance_name}",
        json_data={"where": where, "limit": limit},
    )
