#!/usr/bin/env python3
"""Validate the shared People Work plugin release contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "people-work"
CODEX_MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_MANIFEST = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
MCP_CONFIGURATION = PLUGIN_ROOT / ".mcp.json"
SEMANTIC_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def read_json(path: Path) -> dict[str, object]:
    try:
        contents = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Required file does not exist: {path}") from None
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error}") from error

    if not isinstance(contents, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return contents


def require_mapping(parent: dict[str, object], key: str, path: Path) -> dict[str, object]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"Expected {key} to be an object in {path}")
    return value


def validate() -> str:
    codex = read_json(CODEX_MANIFEST)
    claude = read_json(CLAUDE_MANIFEST)
    mcp = read_json(MCP_CONFIGURATION)

    codex_version = codex.get("version")
    claude_version = claude.get("version")
    if not isinstance(codex_version, str) or not SEMANTIC_VERSION.fullmatch(codex_version):
        raise ValueError(f"Invalid Codex plugin semantic version: {codex_version!r}")
    if claude_version != codex_version:
        raise ValueError(
            "Codex and Claude plugin versions must match: "
            f"{codex_version!r} != {claude_version!r}"
        )

    for manifest, path in ((codex, CODEX_MANIFEST), (claude, CLAUDE_MANIFEST)):
        if manifest.get("name") != "people-work":
            raise ValueError(f"Expected people-work plugin name in {path}")
        if manifest.get("mcpServers") != "./.mcp.json":
            raise ValueError(f"Expected {path} to use the shared ./.mcp.json")

    servers = require_mapping(mcp, "mcpServers", MCP_CONFIGURATION)
    people = require_mapping(servers, "people", MCP_CONFIGURATION)
    if people.get("command") != "people" or people.get("args") != ["mcp"]:
        raise ValueError("Expected the shared MCP server command to be: people mcp")

    icon = PLUGIN_ROOT / "assets" / "people-work-icon.png"
    if not icon.is_file() or icon.stat().st_size == 0:
        raise ValueError(f"Expected a non-empty platform-neutral icon: {icon}")

    return codex_version


def main() -> int:
    try:
        version = validate()
    except ValueError as error:
        print(f"People Work plugin validation failed: {error}", file=sys.stderr)
        return 1

    print(f"People Work plugin {version} is valid for Codex and Claude Code")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
