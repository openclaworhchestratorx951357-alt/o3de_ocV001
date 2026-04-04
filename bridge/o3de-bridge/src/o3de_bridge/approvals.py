"""Approval classification for approved bridge operations."""

from __future__ import annotations

from enum import StrEnum

from .errors import BridgeOperationNotAllowedError
from .models import ApprovalRequirement


class ApprovalLevel(StrEnum):
    """Supported approval levels for the Phase 1 starter scaffold."""

    NONE = "none"
    CONFIRM = "confirm"


_TOOL_APPROVAL_LEVELS: dict[str, ApprovalLevel] = {
    "project_scan": ApprovalLevel.NONE,
    "scene_open": ApprovalLevel.CONFIRM,
    "scene_create": ApprovalLevel.CONFIRM,
    "entity_create": ApprovalLevel.CONFIRM,
    "scene_save": ApprovalLevel.CONFIRM,
    "scene_validate": ApprovalLevel.NONE,
    "get_bridge_capabilities": ApprovalLevel.NONE,
    "bridge_health": ApprovalLevel.NONE,
    "entity_get": ApprovalLevel.NONE,
    "entity_find": ApprovalLevel.NONE,
    "entity_list": ApprovalLevel.NONE,
    "entity_children": ApprovalLevel.NONE,
    "asset_search": ApprovalLevel.NONE,
    "asset_resolve": ApprovalLevel.NONE,
    "component_add": ApprovalLevel.CONFIRM,
    "entity_rename": ApprovalLevel.CONFIRM,
    "entity_set_transform": ApprovalLevel.CONFIRM,
    "mesh_set_model_asset": ApprovalLevel.CONFIRM,
}


def get_approval_requirement(tool_name: str) -> ApprovalRequirement:
    """Return the approval requirement for an approved tool."""

    try:
        approval_level = _TOOL_APPROVAL_LEVELS[tool_name]
    except KeyError as exc:
        raise BridgeOperationNotAllowedError(tool_name=tool_name) from exc

    return ApprovalRequirement(
        tool_name=tool_name,
        approval_level=approval_level.value,
        requires_approval=approval_level is not ApprovalLevel.NONE,
    )


def get_approved_tool_names() -> tuple[str, ...]:
    """Return the ordered set of approved Phase 1 tool names."""

    return tuple(_TOOL_APPROVAL_LEVELS.keys())
