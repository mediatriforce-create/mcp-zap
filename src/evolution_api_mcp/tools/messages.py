"""Message sending tools for Evolution API v1.8.x."""

from typing import Any

from evolution_api_mcp.client import get_client


def _options(
    delay: int | None = None,
    quoted_message_id: str | None = None,
    mentions_everyone: bool = False,
    mentioned: list[str] | None = None,
) -> dict[str, Any]:
    """Build options dict for v1 message body."""
    opts: dict[str, Any] = {}
    if delay is not None:
        opts["delay"] = delay
    if quoted_message_id:
        opts["quotedMessage"] = {"key": {"id": quoted_message_id}}
    if mentions_everyone:
        opts["mentionsEveryOne"] = True
    if mentioned:
        opts["mentioned"] = mentioned
    return opts


async def send_text(
    instance_name: str,
    number: str,
    text: str,
    delay: int | None = None,
    link_preview: bool = True,
    quoted_message_id: str | None = None,
    mentions_everyone: bool = False,
    mentioned: list[str] | None = None,
) -> dict:
    """Send a plain text message on WhatsApp.

    Args:
        instance_name: Name of the connected instance
        number: Recipient phone number with country code (e.g. "5511999999999")
        text: Message text to send
        delay: Delay in milliseconds before sending (simulates typing)
        link_preview: Show link preview if message contains a URL
        quoted_message_id: ID of a message to reply to
        mentions_everyone: Mention all group participants
        mentioned: List of phone numbers to mention
    """
    body: dict[str, Any] = {"number": number}
    body["textMessage"] = {"text": text}
    if not link_preview:
        body["textMessage"]["linkPreview"] = False
    opts = _options(delay, quoted_message_id, mentions_everyone, mentioned)
    if opts:
        body["options"] = opts
    return await get_client().post(
        f"message/sendText/{instance_name}", json_data=body
    )


async def send_media(
    instance_name: str,
    number: str,
    media: str,
    mediatype: str,
    mimetype: str,
    caption: str = "",
    file_name: str = "",
    delay: int | None = None,
    quoted_message_id: str | None = None,
    mentions_everyone: bool = False,
    mentioned: list[str] | None = None,
) -> dict:
    """Send media (image, video, or document) on WhatsApp.

    Args:
        instance_name: Name of the connected instance
        number: Recipient phone number with country code (e.g. "5511999999999")
        media: URL or base64-encoded content of the media
        mediatype: Type of media. Values: image, video, document
        mimetype: MIME type (e.g. "image/png", "video/mp4", "application/pdf")
        caption: Caption text for the media
        file_name: File name (e.g. "photo.png", "report.pdf")
        delay: Delay in milliseconds before sending
        quoted_message_id: ID of a message to reply to
        mentions_everyone: Mention all group participants
        mentioned: List of phone numbers to mention
    """
    body: dict[str, Any] = {"number": number}
    msg: dict[str, Any] = {
        "mediatype": mediatype,
        "mimetype": mimetype,
        "media": media,
    }
    if caption:
        msg["caption"] = caption
    if file_name:
        msg["fileName"] = file_name
    body["mediaMessage"] = msg
    opts = _options(delay, quoted_message_id, mentions_everyone, mentioned)
    if opts:
        body["options"] = opts
    return await get_client().post(
        f"message/sendMedia/{instance_name}", json_data=body
    )


async def send_audio(
    instance_name: str,
    number: str,
    audio: str,
    delay: int | None = None,
    quoted_message_id: str | None = None,
) -> dict:
    """Send an audio message (voice note / PTT) on WhatsApp.

    Args:
        instance_name: Name of the connected instance
        number: Recipient phone number with country code (e.g. "5511999999999")
        audio: URL or base64-encoded audio content
        delay: Delay in milliseconds before sending
        quoted_message_id: ID of a message to reply to
    """
    body: dict[str, Any] = {"number": number}
    body["audioMessage"] = {"audio": audio}
    opts = _options(delay, quoted_message_id)
    if opts:
        body["options"] = opts
    return await get_client().post(
        f"message/sendWhatsAppAudio/{instance_name}", json_data=body
    )


async def send_location(
    instance_name: str,
    number: str,
    latitude: float,
    longitude: float,
    name: str = "",
    address: str = "",
    delay: int | None = None,
    quoted_message_id: str | None = None,
) -> dict:
    """Send a location pin on WhatsApp.

    Args:
        instance_name: Name of the connected instance
        number: Recipient phone number with country code (e.g. "5511999999999")
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        name: Location name (e.g. "Starbucks")
        address: Full address text
        delay: Delay in milliseconds before sending
        quoted_message_id: ID of a message to reply to
    """
    body: dict[str, Any] = {"number": number}
    msg: dict[str, Any] = {"latitude": latitude, "longitude": longitude}
    if name:
        msg["name"] = name
    if address:
        msg["address"] = address
    body["locationMessage"] = msg
    opts = _options(delay, quoted_message_id)
    if opts:
        body["options"] = opts
    return await get_client().post(
        f"message/sendLocation/{instance_name}", json_data=body
    )


async def send_contact(
    instance_name: str,
    number: str,
    contact_name: str,
    contact_number: str,
    contact_org: str = "",
    delay: int | None = None,
    quoted_message_id: str | None = None,
) -> dict:
    """Send a contact card on WhatsApp.

    Args:
        instance_name: Name of the connected instance
        number: Recipient phone number with country code (e.g. "5511999999999")
        contact_name: Full name of the contact to share
        contact_number: Phone number of the contact to share (with country code)
        contact_org: Organization/company name of the contact
        delay: Delay in milliseconds before sending
        quoted_message_id: ID of a message to reply to
    """
    body: dict[str, Any] = {"number": number}
    contact: dict[str, Any] = {
        "fullName": contact_name,
        "wuid": contact_number,
        "phoneNumber": contact_number,
    }
    if contact_org:
        contact["organization"] = contact_org
    body["contactMessage"] = [contact]
    opts = _options(delay, quoted_message_id)
    if opts:
        body["options"] = opts
    return await get_client().post(
        f"message/sendContact/{instance_name}", json_data=body
    )


async def send_reaction(
    instance_name: str,
    number: str,
    message_id: str,
    reaction: str,
    from_me: bool = False,
) -> dict:
    """React to a message with an emoji.

    Args:
        instance_name: Name of the connected instance
        number: Phone number of the chat (with country code)
        message_id: ID of the message to react to
        reaction: Emoji to react with (e.g. "\\ud83d\\udc4d"). Send empty string to remove reaction.
        from_me: True if the message being reacted to was sent by you
    """
    body: dict[str, Any] = {
        "reactionMessage": {
            "key": {
                "remoteJid": f"{number}@s.whatsapp.net",
                "fromMe": from_me,
                "id": message_id,
            },
            "reaction": reaction,
        }
    }
    return await get_client().post(
        f"message/sendReaction/{instance_name}", json_data=body
    )


async def send_poll(
    instance_name: str,
    number: str,
    title: str,
    options: list[str],
    selectable_count: int = 1,
    delay: int | None = None,
) -> dict:
    """Send a poll on WhatsApp.

    Args:
        instance_name: Name of the connected instance
        number: Recipient phone number with country code (e.g. "5511999999999")
        title: Poll question/title
        options: List of poll options (2-12 options)
        selectable_count: How many options can be selected (1 = single choice)
        delay: Delay in milliseconds before sending
    """
    body: dict[str, Any] = {"number": number}
    body["pollMessage"] = {
        "name": title,
        "values": options,
        "selectableCount": selectable_count,
    }
    opts = _options(delay)
    if opts:
        body["options"] = opts
    return await get_client().post(
        f"message/sendPoll/{instance_name}", json_data=body
    )


async def send_buttons(
    instance_name: str,
    number: str,
    title: str,
    description: str,
    footer: str = "",
    buttons: list[dict] | None = None,
    delay: int | None = None,
    quoted_message_id: str | None = None,
) -> dict:
    """Send a message with interactive buttons on WhatsApp.

    Args:
        instance_name: Name of the connected instance
        number: Recipient phone number with country code (e.g. "5511999999999")
        title: Title text of the message
        description: Body/description text of the message
        footer: Footer text (small text at bottom)
        buttons: List of button objects. Each button: {"type": "reply", "reply": {"id": "btn1", "title": "Button Text"}}
        delay: Delay in milliseconds before sending
        quoted_message_id: ID of a message to reply to
    """
    body: dict[str, Any] = {"number": number}
    msg: dict[str, Any] = {"title": title, "description": description}
    if footer:
        msg["footer"] = footer
    if buttons:
        msg["buttons"] = buttons
    body["buttonMessage"] = msg
    opts = _options(delay, quoted_message_id)
    if opts:
        body["options"] = opts
    return await get_client().post(
        f"message/sendButtons/{instance_name}", json_data=body
    )


async def send_list(
    instance_name: str,
    number: str,
    title: str,
    description: str,
    button_text: str,
    sections: list[dict],
    footer: str = "",
    delay: int | None = None,
    quoted_message_id: str | None = None,
) -> dict:
    """Send an interactive list message on WhatsApp.

    Args:
        instance_name: Name of the connected instance
        number: Recipient phone number with country code (e.g. "5511999999999")
        title: Title text of the message
        description: Body/description text
        button_text: Text shown on the list button (e.g. "Ver opcoes")
        sections: List of sections. Each section: {"title": "Section", "rows": [{"title": "Row", "description": "desc", "rowId": "id1"}]}
        footer: Footer text
        delay: Delay in milliseconds before sending
        quoted_message_id: ID of a message to reply to
    """
    body: dict[str, Any] = {"number": number}
    msg: dict[str, Any] = {
        "title": title,
        "description": description,
        "buttonText": button_text,
        "sections": sections,
    }
    if footer:
        msg["footer"] = footer
    body["listMessage"] = msg
    opts = _options(delay, quoted_message_id)
    if opts:
        body["options"] = opts
    return await get_client().post(
        f"message/sendList/{instance_name}", json_data=body
    )


async def send_broadcast(
    instance_name: str,
    numbers: list[str],
    text: str,
    delay: int = 1500,
) -> dict:
    """Send the same text message to multiple WhatsApp numbers at once (broadcast).

    Args:
        instance_name: Name of the connected instance
        numbers: List of phone numbers with country code (e.g. ["5511999999999", "5521888888888"])
        text: Message text to send to all recipients
        delay: Delay in milliseconds between each message to avoid spam detection (default 1500)
    """
    results = []
    for number in numbers:
        result = await get_client().post(
            f"message/sendText/{instance_name}",
            json_data={
                "number": number,
                "textMessage": {"text": text},
                "options": {"delay": delay},
            },
        )
        results.append({"number": number, "result": result})
    return {"sent": len(results), "results": results}


async def edit_message(
    instance_name: str,
    number: str,
    message_id: str,
    new_text: str,
) -> dict:
    """Edit a previously sent WhatsApp text message.

    Args:
        instance_name: Name of the connected instance
        number: Phone number of the chat (with country code, e.g. "5511999999999")
        message_id: ID of the message to edit
        new_text: New text content to replace the original message
    """
    body: dict[str, Any] = {
        "number": number,
        "key": {"id": message_id},
        "text": new_text,
    }
    return await get_client().post(
        f"message/editMessage/{instance_name}", json_data=body
    )


async def forward_message(
    instance_name: str,
    number: str,
    message_id: str,
    remote_jid: str,
    from_me: bool = False,
) -> dict:
    """Forward an existing WhatsApp message to another chat.

    Args:
        instance_name: Name of the connected instance
        number: Recipient phone number to forward to (with country code)
        message_id: ID of the message to forward
        remote_jid: Original chat JID where the message came from
        from_me: Whether the original message was sent by you
    """
    body: dict[str, Any] = {
        "number": number,
        "key": {
            "id": message_id,
            "remoteJid": remote_jid,
            "fromMe": from_me,
        },
    }
    return await get_client().post(
        f"message/forwardMessage/{instance_name}", json_data=body
    )


async def pin_message(
    instance_name: str,
    number: str,
    message_id: str,
    from_me: bool = False,
    pin_duration: int = 86400,
) -> dict:
    """Pin a message in a WhatsApp chat.

    Args:
        instance_name: Name of the connected instance
        number: Phone number of the chat (with country code)
        message_id: ID of the message to pin
        from_me: Whether the message was sent by you
        pin_duration: How long to pin in seconds (86400=24h, 604800=7d, 2592000=30d)
    """
    body: dict[str, Any] = {
        "number": number,
        "key": {
            "id": message_id,
            "remoteJid": f"{number}@s.whatsapp.net",
            "fromMe": from_me,
        },
        "duration": pin_duration,
    }
    return await get_client().post(
        f"message/pinMessage/{instance_name}", json_data=body
    )


async def send_sticker(
    instance_name: str,
    number: str,
    sticker: str,
    delay: int | None = None,
    quoted_message_id: str | None = None,
) -> dict:
    """Send a sticker on WhatsApp.

    Args:
        instance_name: Name of the connected instance
        number: Recipient phone number with country code (e.g. "5511999999999")
        sticker: URL or base64-encoded sticker image (WebP format recommended)
        delay: Delay in milliseconds before sending
        quoted_message_id: ID of a message to reply to
    """
    body: dict[str, Any] = {"number": number}
    body["stickerMessage"] = {"image": sticker}
    opts = _options(delay, quoted_message_id)
    if opts:
        body["options"] = opts
    return await get_client().post(
        f"message/sendSticker/{instance_name}", json_data=body
    )
