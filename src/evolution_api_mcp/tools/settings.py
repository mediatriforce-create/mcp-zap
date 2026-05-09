"""Instance settings and privacy tools for Evolution API v1.8.x."""

from evolution_api_mcp.client import get_client


async def get_instance_settings(instance_name: str) -> dict:
    """Get current settings for a WhatsApp instance.

    Args:
        instance_name: Name of the connected instance
    """
    return await get_client().get(f"instance/fetchSettings/{instance_name}")


async def update_instance_settings(
    instance_name: str,
    reject_call: bool | None = None,
    msg_call: str | None = None,
    groups_ignore: bool | None = None,
    always_online: bool | None = None,
    read_messages: bool | None = None,
    read_status: bool | None = None,
    sync_full_history: bool | None = None,
) -> dict:
    """Update settings for a WhatsApp instance.

    Args:
        instance_name: Name of the connected instance
        reject_call: Automatically reject incoming calls
        msg_call: Message to send when rejecting a call (e.g. "Não posso atender agora")
        groups_ignore: Ignore messages from groups
        always_online: Always show as online
        read_messages: Automatically mark messages as read
        read_status: Automatically mark status as viewed
        sync_full_history: Sync full message history on connect
    """
    body: dict = {}
    if reject_call is not None:
        body["rejectCall"] = reject_call
    if msg_call is not None:
        body["msgCall"] = msg_call
    if groups_ignore is not None:
        body["groupsIgnore"] = groups_ignore
    if always_online is not None:
        body["alwaysOnline"] = always_online
    if read_messages is not None:
        body["readMessages"] = read_messages
    if read_status is not None:
        body["readStatus"] = read_status
    if sync_full_history is not None:
        body["syncFullHistory"] = sync_full_history

    return await get_client().post(
        f"instance/setSettings/{instance_name}", json_data=body
    )


async def get_privacy_settings(instance_name: str) -> dict:
    """Get privacy settings of the WhatsApp account (last seen, profile photo, status visibility, etc).

    Args:
        instance_name: Name of the connected instance
    """
    return await get_client().get(f"instance/fetchPrivacySettings/{instance_name}")


async def update_privacy_settings(
    instance_name: str,
    read_receipts: str | None = None,
    profile: str | None = None,
    status: str | None = None,
    online: str | None = None,
    last_seen: str | None = None,
    groups_add: str | None = None,
) -> dict:
    """Update privacy settings of the WhatsApp account.

    Args:
        instance_name: Name of the connected instance
        read_receipts: Who can see read receipts. Values: all, none
        profile: Who can see profile photo. Values: all, contacts, contact_blacklist, none
        status: Who can see status/stories. Values: all, contacts, contact_blacklist, none
        online: Who can see when you're online. Values: all, match_last_seen
        last_seen: Who can see your last seen. Values: all, contacts, contact_blacklist, none
        groups_add: Who can add you to groups. Values: all, contacts, contact_blacklist, none
    """
    body: dict = {}
    if read_receipts is not None:
        body["readreceipts"] = read_receipts
    if profile is not None:
        body["profile"] = profile
    if status is not None:
        body["status"] = status
    if online is not None:
        body["online"] = online
    if last_seen is not None:
        body["last"] = last_seen
    if groups_add is not None:
        body["groupadd"] = groups_add

    return await get_client().put(
        f"instance/updatePrivacySettings/{instance_name}", json_data=body
    )
