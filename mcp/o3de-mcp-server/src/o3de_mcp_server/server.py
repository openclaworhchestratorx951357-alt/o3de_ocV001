"""Minimal MCP server-side exposure path for foundational O3DE tools."""

from __future__ import annotations

from typing import Any

from .registry import invoke_registered_tool

EXPOSED_TOOL_NAMES: tuple[str, ...] = (
    "get_bridge_capabilities",
    "bridge_health",
    "project_scan",
    "scene_open",
    "scene_create",
    "scene_save",
    "scene_validate",
    "entity_create",
    "entity_get",
    "entity_find",
    "asset_search",
    "asset_resolve",
    "component_add",
    "entity_rename",
    "entity_set_transform",
    "mesh_set_model_asset",
)


class ServerExposureError(KeyError):
    """Deterministic server-layer rejection for non-exposed tools."""


def list_exposed_tools() -> tuple[str, ...]:
    return EXPOSED_TOOL_NAMES


def handle_tool_call(tool_name: str, payload: dict[str, Any] | None) -> Any:
    if tool_name not in EXPOSED_TOOL_NAMES:
        raise ServerExposureError(tool_name)
    return invoke_registered_tool(tool_name, payload)
