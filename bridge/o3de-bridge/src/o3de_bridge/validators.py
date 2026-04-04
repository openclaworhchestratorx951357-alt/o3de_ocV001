"""Deterministic validation for approved bridge requests."""

from __future__ import annotations

import re
from typing import Any

from .approvals import get_approval_requirement, get_approved_tool_names
from .errors import (
    APPROVAL_REQUIRED,
    INVALID_COMPONENT,
    INVALID_ENTITY_NAME,
    INVALID_PROJECT_ID,
    INVALID_REQUEST,
    INVALID_SCENE_NAME,
    TOOL_NOT_ALLOWED,
    BridgeValidationError,
)
from .models import (
    AssetResolveRequest,
    AssetSearchRequest,
    BridgeHealthRequest,
    ComponentAddRequest,
    ComponentSpec,
    EntityChildrenRequest,
    EntityCreateRequest,
    EntityFindRequest,
    EntityGetRequest,
    EntityListRequest,
    EntityRenameRequest,
    EntitySetTransformRequest,
    GetBridgeCapabilitiesRequest,
    MeshSetModelAssetRequest,
    ProjectScanRequest,
    RequestMeta,
    SceneCreateRequest,
    SceneOpenRequest,
    SceneSaveRequest,
    SceneValidateRequest,
)

_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
_ALLOWED_REQUEST_TYPES: dict[str, type] = {
    "project_scan": ProjectScanRequest,
    "scene_open": SceneOpenRequest,
    "scene_create": SceneCreateRequest,
    "entity_create": EntityCreateRequest,
    "scene_save": SceneSaveRequest,
    "scene_validate": SceneValidateRequest,
    "get_bridge_capabilities": GetBridgeCapabilitiesRequest,
    "bridge_health": BridgeHealthRequest,
    "entity_get": EntityGetRequest,
    "entity_find": EntityFindRequest,
    "entity_list": EntityListRequest,
    "entity_children": EntityChildrenRequest,
    "asset_search": AssetSearchRequest,
    "asset_resolve": AssetResolveRequest,
    "component_add": ComponentAddRequest,
    "entity_rename": EntityRenameRequest,
    "entity_set_transform": EntitySetTransformRequest,
    "mesh_set_model_asset": MeshSetModelAssetRequest,
}


def validate_tool_name(tool_name: str) -> None:
    """Validate that the tool name is part of the approved six-tool surface."""

    if tool_name not in get_approved_tool_names():
        raise BridgeValidationError(
            code=TOOL_NOT_ALLOWED,
            message=f"Unsupported tool name: {tool_name}",
            target="tool_name",
        )


def validate_request_meta(meta: RequestMeta) -> None:
    """Validate shared request metadata."""

    validate_tool_name(meta.tool_name)

    if not meta.request_id.strip():
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="request_id must be a non-empty string.",
            target="request_id",
        )


def validate_project_id(project_id: str) -> None:
    """Validate project identifiers."""

    if not _IDENTIFIER_PATTERN.fullmatch(project_id):
        raise BridgeValidationError(
            code=INVALID_PROJECT_ID,
            message=f"Invalid project_id: {project_id}",
            target="project_id",
        )


def validate_scene_name(scene_name: str) -> None:
    """Validate scene names."""

    if not _IDENTIFIER_PATTERN.fullmatch(scene_name):
        raise BridgeValidationError(
            code=INVALID_SCENE_NAME,
            message=f"Invalid scene_name: {scene_name}",
            target="scene_name",
        )


def validate_entity_name(entity_name: str) -> None:
    """Validate entity names."""

    if not _IDENTIFIER_PATTERN.fullmatch(entity_name):
        raise BridgeValidationError(
            code=INVALID_ENTITY_NAME,
            message=f"Invalid entity_name: {entity_name}",
            target="entity_name",
        )


def validate_component_specs(components: list[ComponentSpec]) -> None:
    """Validate entity component specs for the approved v1 component set."""

    for component in components:
        if component.type not in {"Camera", "Mesh"}:
            raise BridgeValidationError(
                code=INVALID_COMPONENT,
                message=f"Unsupported component type: {component.type}",
                target="components",
            )


def validate_approval_token(meta: RequestMeta) -> None:
    """Require non-blank approval token presence for approval-gated tools."""

    approval = get_approval_requirement(meta.tool_name)
    approval_token = meta.approval_token.strip() if meta.approval_token is not None else ""
    if approval.requires_approval and not approval_token:
        raise BridgeValidationError(
            code=APPROVAL_REQUIRED,
            message=f"approval_token is required for tool: {meta.tool_name}",
            target="approval_token",
        )


def validate_get_bridge_capabilities_request(request_model: GetBridgeCapabilitiesRequest) -> None:
    """Validate get_bridge_capabilities specific request requirements."""

    validate_request_meta(request_model.meta)
    validate_project_id(request_model.project_id)


def validate_bridge_health_request(request_model: BridgeHealthRequest) -> None:
    """Validate bridge_health specific request requirements."""

    validate_request_meta(request_model.meta)
    if request_model.project_id is not None:
        validate_project_id(request_model.project_id)


def validate_entity_get_request(request_model: EntityGetRequest) -> None:
    """Validate entity_get specific request requirements."""

    validate_request_meta(request_model.meta)
    validate_project_id(request_model.project_id)
    if request_model.scene_name is not None:
        validate_scene_name(request_model.scene_name)
    if not request_model.entity_id.strip():
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="entity_id must be a non-empty string.",
            target="entity_id",
        )


def validate_entity_find_request(request_model: EntityFindRequest) -> None:
    """Validate entity_find specific request requirements."""

    validate_request_meta(request_model.meta)
    validate_project_id(request_model.project_id)
    if request_model.scene_name is not None:
        validate_scene_name(request_model.scene_name)
    query = request_model.query
    entity_name = query.entity_name.strip() if query.entity_name is not None else ""
    entity_id = query.entity_id.strip() if query.entity_id is not None else ""
    if not entity_name and not entity_id:
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="entity_find requires entity_name or entity_id search criteria.",
            target="query",
        )
    if query.match_mode not in {"exact", "prefix", "contains"}:
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message=f"Unsupported match_mode: {query.match_mode}",
            target="query.match_mode",
        )


def validate_entity_list_request(request_model: EntityListRequest) -> None:
    """Validate entity_list specific request requirements."""

    validate_request_meta(request_model.meta)
    validate_project_id(request_model.project_id)
    if request_model.scene_name is not None:
        validate_scene_name(request_model.scene_name)
    if request_model.scope not in {"scene", "root_only", "children_only"}:
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message=f"Unsupported scope: {request_model.scope}",
            target="scope",
        )


def validate_entity_children_request(request_model: EntityChildrenRequest) -> None:
    """Validate entity_children specific request requirements."""

    validate_request_meta(request_model.meta)
    validate_project_id(request_model.project_id)
    if request_model.scene_name is not None:
        validate_scene_name(request_model.scene_name)
    if not request_model.parent_entity_id.strip():
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="parent_entity_id must be a non-empty string.",
            target="parent_entity_id",
        )


def validate_asset_search_request(request_model: AssetSearchRequest) -> None:
    """Validate asset_search specific request requirements."""

    validate_request_meta(request_model.meta)
    validate_project_id(request_model.project_id)
    if not request_model.query.strip():
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="query must be a non-empty string.",
            target="query",
        )


def validate_asset_resolve_request(request_model: AssetResolveRequest) -> None:
    """Validate asset_resolve specific request requirements."""

    validate_request_meta(request_model.meta)
    validate_project_id(request_model.project_id)
    asset_id = request_model.asset_id.strip() if request_model.asset_id is not None else ""
    asset_hint = request_model.asset_hint.strip() if request_model.asset_hint is not None else ""
    if not asset_id and not asset_hint:
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="asset_id or asset_hint must be provided.",
            target="asset_resolve",
        )


def validate_component_add_request(request_model: ComponentAddRequest) -> None:
    """Validate component_add specific request requirements."""

    validate_request_meta(request_model.meta)
    validate_project_id(request_model.project_id)
    if request_model.scene_name is not None:
        validate_scene_name(request_model.scene_name)
    if not request_model.entity_id.strip():
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="entity_id must be a non-empty string.",
            target="entity_id",
        )
    if not request_model.component_type.strip():
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="component_type must be a non-empty string.",
            target="component_type",
        )


def validate_entity_rename_request(request_model: EntityRenameRequest) -> None:
    """Validate entity_rename specific request requirements."""

    validate_request_meta(request_model.meta)
    validate_project_id(request_model.project_id)
    if request_model.scene_name is not None:
        validate_scene_name(request_model.scene_name)
    if not request_model.entity_id.strip():
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="entity_id must be a non-empty string.",
            target="entity_id",
        )
    if not request_model.new_name.strip():
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="new_name must be a non-empty string.",
            target="new_name",
        )


def validate_entity_set_transform_request(request_model: EntitySetTransformRequest) -> None:
    """Validate entity_set_transform specific request requirements."""

    validate_request_meta(request_model.meta)
    validate_project_id(request_model.project_id)
    if request_model.scene_name is not None:
        validate_scene_name(request_model.scene_name)
    if not request_model.entity_id.strip():
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="entity_id must be a non-empty string.",
            target="entity_id",
        )
    transform = request_model.transform
    if (
        transform.translation is None
        and transform.rotation_euler_degrees is None
        and transform.scale is None
    ):
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="transform must include at least one of translation, rotation_euler_degrees, or scale.",
            target="transform",
        )


def validate_mesh_set_model_asset_request(request_model: MeshSetModelAssetRequest) -> None:
    """Validate mesh_set_model_asset specific request requirements."""

    validate_request_meta(request_model.meta)
    validate_project_id(request_model.project_id)
    if request_model.scene_name is not None:
        validate_scene_name(request_model.scene_name)
    if not request_model.entity_id.strip():
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="entity_id must be a non-empty string.",
            target="entity_id",
        )
    if not request_model.model_asset.model_asset_path.strip():
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message="model_asset_path must be a non-empty string.",
            target="model_asset.model_asset_path",
        )


def validate_request_model(tool_name: str, request_model: Any) -> None:
    """Validate a request model against the approved tool surface and model map."""

    validate_tool_name(tool_name)

    expected_type = _ALLOWED_REQUEST_TYPES[tool_name]
    if not isinstance(request_model, expected_type):
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message=(
                f"Request model type mismatch for {tool_name}: "
                f"expected {expected_type.__name__}, got {type(request_model).__name__}"
            ),
            target="request_model",
        )

    validate_request_meta(request_model.meta)

    if request_model.meta.tool_name != tool_name:
        raise BridgeValidationError(
            code=INVALID_REQUEST,
            message=(
                f"Request metadata tool_name '{request_model.meta.tool_name}' "
                f"does not match dispatch tool_name '{tool_name}'."
            ),
            target="meta.tool_name",
        )

    if tool_name == "get_bridge_capabilities":
        validate_get_bridge_capabilities_request(request_model)
        return

    if tool_name == "bridge_health":
        validate_bridge_health_request(request_model)
        return

    if tool_name == "entity_get":
        validate_entity_get_request(request_model)
        return

    if tool_name == "entity_find":
        validate_entity_find_request(request_model)
        return

    if tool_name == "entity_list":
        validate_entity_list_request(request_model)
        return

    if tool_name == "entity_children":
        validate_entity_children_request(request_model)
        return

    if tool_name == "asset_search":
        validate_asset_search_request(request_model)
        return

    if tool_name == "asset_resolve":
        validate_asset_resolve_request(request_model)
        return

    if tool_name == "component_add":
        validate_component_add_request(request_model)
        return

    if tool_name == "entity_rename":
        validate_entity_rename_request(request_model)
        return

    if tool_name == "entity_set_transform":
        validate_entity_set_transform_request(request_model)
        return

    if tool_name == "mesh_set_model_asset":
        validate_mesh_set_model_asset_request(request_model)
        return

    validate_approval_token(request_model.meta)
    validate_project_id(request_model.project_id)

    if hasattr(request_model, "scene_name"):
        validate_scene_name(request_model.scene_name)

    if hasattr(request_model, "entity_name"):
        validate_entity_name(request_model.entity_name)

    if hasattr(request_model, "components"):
        validate_component_specs(request_model.components)
