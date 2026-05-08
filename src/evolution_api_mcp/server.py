"""Evolution API MCP server — WhatsApp messaging via Evolution API."""

import importlib
import inspect
import pkgutil

from fastmcp import FastMCP
from fastmcp.experimental.transforms.code_mode import CodeMode, MontySandboxProvider

mcp = FastMCP(
    "evolution-api",
    instructions=(
        "WhatsApp messaging server via Evolution API. "
        "Use instance tools to create/connect a WhatsApp instance (scan QR code), "
        "then use message tools to send text, media, audio, location, contacts, "
        "polls, buttons, lists, stickers, and reactions. "
        "Chat tools let you list conversations and read message history."
    ),
)

# Auto-discover and register all tools from the tools package
import evolution_api_mcp.tools as tools_pkg

for _importer, module_name, _ispkg in pkgutil.iter_modules(tools_pkg.__path__):
    fqn = f"evolution_api_mcp.tools.{module_name}"
    module = importlib.import_module(fqn)
    for name, func in inspect.getmembers(module, inspect.isfunction):
        if not name.startswith("_") and func.__module__ == fqn:
            mcp.tool(func)

# Code Mode: collapses all tools into 3 meta-tools (search, get_schema, execute)
sandbox = MontySandboxProvider(
    limits={"max_duration_secs": 30, "max_memory": 100_000_000},
)
mcp.add_transform(CodeMode(sandbox_provider=sandbox))


def main():
    """CLI entry point."""
    mcp.run()


if __name__ == "__main__":
    main()
