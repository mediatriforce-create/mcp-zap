"""Instance management tools for Evolution API."""

from evolution_api_mcp.client import get_client


async def create_instance(
    instance_name: str,
    integration: str = "WHATSAPP-BAILEYS",
    qrcode: bool = True,
    number: str | None = None,
) -> dict:
    """Create a new WhatsApp instance.

    Args:
        instance_name: Name for the instance (e.g. "my-whatsapp")
        integration: Integration type. Values: WHATSAPP-BAILEYS, WHATSAPP-BUSINESS
        qrcode: If True, returns QR code in the response for immediate connection
        number: Optional phone number with country code (e.g. "5511999999999")
    """
    body: dict = {
        "instanceName": instance_name,
        "integration": integration,
        "qrcode": qrcode,
    }
    if number:
        body["number"] = number
    return await get_client().post("instance/create", json_data=body)


async def connect_instance(instance_name: str) -> dict:
    """Connect an instance and get the QR code to scan with WhatsApp.

    Args:
        instance_name: Name of the instance to connect
    """
    return await get_client().get(f"instance/connect/{instance_name}")


async def fetch_instances(instance_name: str | None = None) -> dict:
    """List all instances or get details of a specific instance.

    Args:
        instance_name: Optional instance name to filter. If None, returns all instances.
    """
    endpoint = "instance/fetchInstances"
    if instance_name:
        endpoint += f"/{instance_name}"
    return await get_client().get(endpoint)


async def connection_state(instance_name: str) -> dict:
    """Check the connection state of an instance.

    Args:
        instance_name: Name of the instance
    """
    return await get_client().get(f"instance/connectionState/{instance_name}")


async def logout_instance(instance_name: str) -> dict:
    """Logout from WhatsApp (disconnect but keep the instance).

    Args:
        instance_name: Name of the instance to logout
    """
    return await get_client().delete(f"instance/logout/{instance_name}")


async def restart_instance(instance_name: str) -> dict:
    """Restart an instance.

    Args:
        instance_name: Name of the instance to restart
    """
    return await get_client().put(f"instance/restart/{instance_name}")


async def delete_instance(instance_name: str) -> dict:
    """Delete an instance permanently.

    Args:
        instance_name: Name of the instance to delete
    """
    return await get_client().delete(f"instance/delete/{instance_name}")


async def set_presence(instance_name: str, presence: str) -> dict:
    """Set the presence status of the instance.

    Args:
        instance_name: Name of the instance
        presence: Presence status. Values: available, unavailable, composing, recording, paused
    """
    return await get_client().post(
        f"instance/setPresence/{instance_name}",
        json_data={"presence": presence},
    )
