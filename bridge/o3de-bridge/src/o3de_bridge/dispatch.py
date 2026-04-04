"""Whitelist-only dispatch for the approved six-tool bridge surface."""

from __future__ import annotations

from collections.abc import Callable

from .approvals import get_approval_requirement
from .capabilities import build_baseline_capabilities
from .models import (
    AddedComponentRecord,
    AppliedTransformRecord,
    AssetRecord,
    AssetResolveData,
    AssetResolveRequest,
    AssetResolveResponse,
    AssetSearchData,
    AssetSearchRequest,
    AssetSearchResponse,
    BridgeHealthData,
    BridgeHealthRequest,
    BridgeHealthResponse,
    CapabilityEnvelopeData,
    ComponentAddData,
    ComponentAddRequest,
    ComponentAddResponse,
    EditorState,
    EntityComponentSummary,
    EntityCreateData,
    EntityCreateRequest,
    EntityFindData,
    EntityFindRequest,
    EntityFindResponse,
    EntityFindResultRecord,
    EntityGetData,
    EntityGetRequest,
    EntityGetResponse,
    EntityRecord,
    EntityRenameData,
    EntityRenameRequest,
    EntityRenameResponse,
    EntitySetTransformData,
    EntitySetTransformRequest,
    EntitySetTransformResponse,
    GetBridgeCapabilitiesRequest,
    MeshSetModelAssetData,
    MeshSetModelAssetRequest,
    MeshSetModelAssetResponse,
    GetBridgeCapabilitiesResponse,
    LogEntry,
    OperationResult,
    ProjectScanData,
    ProjectScanRequest,
    RenamedEntityRecord,
    SceneCreateData,
    SceneCreateRequest,
    SceneOpenData,
    SceneOpenRequest,
    SceneSaveData,
    SceneSaveRequest,
    SceneValidateData,
    SceneValidateRequest,
)
from .validators import validate_request_model, validate_tool_name

DispatchRequest = (
    ProjectScanRequest
    | SceneOpenRequest
    | SceneCreateRequest
    | EntityCreateRequest
    | SceneSaveRequest
    | SceneValidateRequest
    | GetBridgeCapabilitiesRequest
    | BridgeHealthRequest
    | EntityGetRequest
    | EntityFindRequest
    | AssetSearchRequest
    | AssetResolveRequest
    | ComponentAddRequest
    | EntityRenameRequest
    | EntitySetTransformRequest
    | MeshSetModelAssetRequest
)

DispatchHandler = Callable[[DispatchRequest], OperationResult]


def _base_result(tool_name: str, request: DispatchRequest) -> dict[str, object]:
    """Build shared deterministic result metadata for stub handlers."""

    approval = get_approval_requirement(tool_name)
    return {
        "request_id": request.meta.request_id,
        "tool_name": tool_name,
        "ok": True,
        "warnings": [],
        "errors": [],
        "logs": [
            LogEntry(
                level="info",
                message=f"Stub handler executed for {tool_name}.",
                code=None,
                target=None,
            )
        ],
        "requires_approval": approval.requires_approval,
        "approval_level": approval.approval_level,
    }


def _handle_project_scan(request: ProjectScanRequest) -> OperationResult:
    """Deterministic stub handler for project_scan."""

    return OperationResult(
        **_base_result("project_scan", request),
        data=ProjectScanData(
            project_id=request.project_id,
            project_found=True,
            scenes=[],
            assets=[],
            editor_state=EditorState(running=False),
        ),
    )


def _handle_scene_open(request: SceneOpenRequest) -> OperationResult:
    """Deterministic stub handler for scene_open."""

    return OperationResult(
        **_base_result("scene_open", request),
        data=SceneOpenData(
            project_id=request.project_id,
            scene_name=request.scene_name,
            opened=False,
            already_open=False,
        ),
    )


def _handle_scene_create(request: SceneCreateRequest) -> OperationResult:
    """Deterministic stub handler for scene_create."""

    return OperationResult(
        **_base_result("scene_create", request),
        data=SceneCreateData(
            project_id=request.project_id,
            scene_name=request.scene_name,
            created=False,
        ),
    )


def _handle_entity_create(request: EntityCreateRequest) -> OperationResult:
    """Deterministic stub handler for entity_create."""

    return OperationResult(
        **_base_result("entity_create", request),
        data=EntityCreateData(
            project_id=request.project_id,
            scene_name=request.scene_name,
            entity_name=request.entity_name,
            entity_created=False,
            components_added=[],
        ),
    )


def _handle_scene_save(request: SceneSaveRequest) -> OperationResult:
    """Deterministic stub handler for scene_save."""

    return OperationResult(
        **_base_result("scene_save", request),
        data=SceneSaveData(
            project_id=request.project_id,
            scene_name=request.scene_name,
            saved=False,
        ),
    )


def _handle_scene_validate(request: SceneValidateRequest) -> OperationResult:
    """Deterministic stub handler for scene_validate."""

    return OperationResult(
        **_base_result("scene_validate", request),
        data=SceneValidateData(
            project_id=request.project_id,
            scene_name=request.scene_name,
            valid=False,
            issues=[],
            entities=[],
        ),
    )


def _handle_get_bridge_capabilities(request: GetBridgeCapabilitiesRequest) -> GetBridgeCapabilitiesResponse:
    """Deterministic baseline handler for get_bridge_capabilities."""

    capability_data = build_baseline_capabilities(
        project_name=request.project_id,
        generated_at=request.meta.timestamp or "unknown",
    )
    base = _base_result("get_bridge_capabilities", request)
    return GetBridgeCapabilitiesResponse(
        request_id=base["request_id"],
        tool_name="get_bridge_capabilities",
        ok=True,
        data=CapabilityEnvelopeData(bridge_capabilities=capability_data),
        warnings=base["warnings"],
        errors=base["errors"],
        logs=base["logs"],
        requires_approval=base["requires_approval"],
        approval_level=base["approval_level"],
    )


def _handle_bridge_health(request: BridgeHealthRequest) -> BridgeHealthResponse:
    """Deterministic baseline handler for bridge_health."""

    base = _base_result("bridge_health", request)
    return BridgeHealthResponse(
        request_id=base["request_id"],
        tool_name="bridge_health",
        ok=True,
        data=BridgeHealthData(
            bridge_version="1.0.0",
            transport_ready=True,
            bootstrap_installed=False,
            live_session_connected=False,
            registered_handlers=sorted(_DISPATCH_HANDLERS.keys()),
        ),
        warnings=base["warnings"],
        errors=base["errors"],
        logs=base["logs"],
        requires_approval=base["requires_approval"],
        approval_level=base["approval_level"],
    )


def _handle_entity_get(request: EntityGetRequest) -> EntityGetResponse:
    """Deterministic baseline handler for entity_get."""

    base = _base_result("entity_get", request)
    return EntityGetResponse(
        request_id=base["request_id"],
        tool_name="entity_get",
        ok=True,
        data=EntityGetData(
            project_id=request.project_id,
            scene_name=request.scene_name,
            entity=EntityRecord(
                entity_id=request.entity_id,
                entity_name="stub_entity",
                scene_name=request.scene_name,
                exists=False,
                transform=None,
                components=[EntityComponentSummary(component_type="placeholder", enabled=True)],
            ),
        ),
        warnings=base["warnings"],
        errors=base["errors"],
        logs=base["logs"],
        requires_approval=base["requires_approval"],
        approval_level=base["approval_level"],
    )


def _handle_entity_find(request: EntityFindRequest) -> EntityFindResponse:
    """Deterministic inspection-only baseline handler for entity_find."""

    base = _base_result("entity_find", request)
    query = request.query
    entity_name = (query.entity_name or "").strip()
    entity_id = (query.entity_id or "").strip()

    stub_entities = [
        EntityFindResultRecord(
            entity_id="entity-001",
            entity_name="test_entity",
            scene_name=request.scene_name,
            match_reason="entity_name_exact",
        ),
        EntityFindResultRecord(
            entity_id="entity-002",
            entity_name="test_entity_camera",
            scene_name=request.scene_name,
            match_reason="entity_name_prefix",
        ),
        EntityFindResultRecord(
            entity_id="entity-003",
            entity_name="bridge_test_entity",
            scene_name=request.scene_name,
            match_reason="entity_name_contains",
        ),
    ]

    if entity_id:
        matches = [
            EntityFindResultRecord(
                entity_id=entity_id,
                entity_name="stub_entity",
                scene_name=request.scene_name,
                match_reason="entity_id_exact",
            )
        ]
    elif query.match_mode == "exact":
        matches = [record for record in stub_entities if record.entity_name == entity_name]
    elif query.match_mode == "prefix":
        matches = [record for record in stub_entities if record.entity_name.startswith(entity_name)]
    else:
        matches = [record for record in stub_entities if entity_name in record.entity_name]

    matches = sorted(matches, key=lambda record: (record.entity_name, record.entity_id))[: query.limit]
    query_summary = f"entity_id={entity_id}" if entity_id else f"entity_name={entity_name}"

    return EntityFindResponse(
        request_id=base["request_id"],
        tool_name="entity_find",
        ok=True,
        data=EntityFindData(
            project_id=request.project_id,
            scene_name=request.scene_name,
            match_mode=query.match_mode,
            query_summary=query_summary,
            total_matches=len(matches),
            matches=matches,
        ),
        warnings=base["warnings"],
        errors=base["errors"],
        logs=base["logs"],
        requires_approval=base["requires_approval"],
        approval_level=base["approval_level"],
    )


def _handle_asset_search(request: AssetSearchRequest) -> AssetSearchResponse:
    """Deterministic inspection-only baseline handler for asset_search."""

    base = _base_result("asset_search", request)
    return AssetSearchResponse(
        request_id=base["request_id"],
        tool_name="asset_search",
        ok=True,
        data=AssetSearchData(
            project_id=request.project_id,
            query=request.query,
            matches=[
                AssetRecord(
                    asset_id="asset-001",
                    asset_path="objects/_primitives/_box_1x1.fbx.azmodel",
                    asset_category="model",
                    resolved=True,
                )
            ],
        ),
        warnings=base["warnings"],
        errors=base["errors"],
        logs=base["logs"],
        requires_approval=base["requires_approval"],
        approval_level=base["approval_level"],
    )


def _handle_asset_resolve(request: AssetResolveRequest) -> AssetResolveResponse:
    """Deterministic inspection-only baseline handler for asset_resolve."""

    base = _base_result("asset_resolve", request)
    asset_key = request.asset_id or request.asset_hint or "unresolved"
    return AssetResolveResponse(
        request_id=base["request_id"],
        tool_name="asset_resolve",
        ok=True,
        data=AssetResolveData(
            project_id=request.project_id,
            asset=AssetRecord(
                asset_id=request.asset_id or "asset-001",
                asset_path=str(asset_key),
                asset_category="model",
                resolved=True,
            ),
            resolution_status="resolved",
        ),
        warnings=base["warnings"],
        errors=base["errors"],
        logs=base["logs"],
        requires_approval=base["requires_approval"],
        approval_level=base["approval_level"],
    )


def _handle_component_add(request: ComponentAddRequest) -> ComponentAddResponse:
    """Deterministic fail-closed baseline handler for component_add."""

    base = _base_result("component_add", request)
    allowed_component_types = {"Camera", "Mesh"}
    component_allowed = request.component_type in allowed_component_types
    outcome_status = "rejected_unapproved_mutation"
    extra_logs = []

    if not component_allowed:
        outcome_status = "rejected_disallowed_component_type"
        extra_logs.append(
            LogEntry(
                level="warning",
                message=f"component_add rejected unsupported component type: {request.component_type}",
                code="component_type_not_allowed",
                target="component_type",
            )
        )

    return ComponentAddResponse(
        request_id=base["request_id"],
        tool_name="component_add",
        ok=False,
        data=ComponentAddData(
            project_id=request.project_id,
            scene_name=request.scene_name,
            entity_id=request.entity_id,
            outcome_status=outcome_status,
            added_component=AddedComponentRecord(
                component_type=request.component_type,
                component_id=None,
                added=False,
                approval_required=True,
            ),
        ),
        warnings=base["warnings"],
        errors=base["errors"],
        logs=base["logs"] + extra_logs,
        requires_approval=base["requires_approval"],
        approval_level=base["approval_level"],
    )


def _handle_entity_rename(request: EntityRenameRequest) -> EntityRenameResponse:
    """Deterministic fail-closed baseline handler for entity_rename."""

    base = _base_result("entity_rename", request)
    outcome_status = "rejected_unapproved_mutation"
    extra_logs = []

    if request.current_name is not None and request.current_name == request.new_name:
        outcome_status = "rejected_invalid_rename"
        extra_logs.append(
            LogEntry(
                level="warning",
                message="entity_rename rejected because new_name matches current_name.",
                code="rename_noop_not_allowed",
                target="new_name",
            )
        )

    return EntityRenameResponse(
        request_id=base["request_id"],
        tool_name="entity_rename",
        ok=False,
        data=EntityRenameData(
            project_id=request.project_id,
            scene_name=request.scene_name,
            entity_id=request.entity_id,
            outcome_status=outcome_status,
            renamed_entity=RenamedEntityRecord(
                entity_id=request.entity_id,
                old_name=request.current_name or "unknown",
                new_name=request.new_name,
                renamed=False,
                approval_required=True,
            ),
        ),
        warnings=base["warnings"],
        errors=base["errors"],
        logs=base["logs"] + extra_logs,
        requires_approval=base["requires_approval"],
        approval_level=base["approval_level"],
    )


def _handle_entity_set_transform(request: EntitySetTransformRequest) -> EntitySetTransformResponse:
    """Deterministic fail-closed baseline handler for entity_set_transform."""

    base = _base_result("entity_set_transform", request)
    outcome_status = "rejected_unapproved_mutation"
    extra_logs = []

    if request.transform.translation == (0.0, 0.0, 0.0):
        outcome_status = "rejected_invalid_transform"
        extra_logs.append(
            LogEntry(
                level="warning",
                message="entity_set_transform rejected zero translation baseline payload.",
                code="transform_not_allowed",
                target="transform.translation",
            )
        )

    return EntitySetTransformResponse(
        request_id=base["request_id"],
        tool_name="entity_set_transform",
        ok=False,
        data=EntitySetTransformData(
            project_id=request.project_id,
            scene_name=request.scene_name,
            entity_id=request.entity_id,
            outcome_status=outcome_status,
            applied_transform=AppliedTransformRecord(
                entity_id=request.entity_id,
                transform=request.transform,
                applied=False,
                approval_required=True,
            ),
        ),
        warnings=base["warnings"],
        errors=base["errors"],
        logs=base["logs"] + extra_logs,
        requires_approval=base["requires_approval"],
        approval_level=base["approval_level"],
    )


def _handle_mesh_set_model_asset(request: MeshSetModelAssetRequest) -> MeshSetModelAssetResponse:
    """Deterministic fail-closed baseline handler for mesh_set_model_asset."""

    base = _base_result("mesh_set_model_asset", request)
    outcome_status = "rejected_unapproved_mutation"
    extra_logs = []

    if not request.model_asset.model_asset_path.lower().endswith((".azmodel", ".fbx")):
        outcome_status = "rejected_disallowed_model_asset"
        extra_logs.append(
            LogEntry(
                level="warning",
                message="mesh_set_model_asset rejected unsupported model asset target.",
                code="model_asset_not_allowed",
                target="model_asset.model_asset_path",
            )
        )

    return MeshSetModelAssetResponse(
        request_id=base["request_id"],
        tool_name="mesh_set_model_asset",
        ok=False,
        data=MeshSetModelAssetData(
            project_id=request.project_id,
            scene_name=request.scene_name,
            entity_id=request.entity_id,
            outcome_status=outcome_status,
            assigned_model_asset=AssignedModelAssetRecord(
                entity_id=request.entity_id,
                model_asset=request.model_asset,
                assigned=False,
                approval_required=True,
            ),
        ),
        warnings=base["warnings"],
        errors=base["errors"],
        logs=base["logs"] + extra_logs,
        requires_approval=base["requires_approval"],
        approval_level=base["approval_level"],
    )


_DISPATCH_HANDLERS: dict[str, DispatchHandler] = {
    "project_scan": _handle_project_scan,
    "scene_open": _handle_scene_open,
    "scene_create": _handle_scene_create,
    "entity_create": _handle_entity_create,
    "scene_save": _handle_scene_save,
    "scene_validate": _handle_scene_validate,
    "get_bridge_capabilities": _handle_get_bridge_capabilities,
    "bridge_health": _handle_bridge_health,
    "entity_get": _handle_entity_get,
    "entity_find": _handle_entity_find,
    "asset_search": _handle_asset_search,
    "asset_resolve": _handle_asset_resolve,
    "component_add": _handle_component_add,
    "entity_rename": _handle_entity_rename,
    "entity_set_transform": _handle_entity_set_transform,
    "mesh_set_model_asset": _handle_mesh_set_model_asset,
}


def dispatch(tool_name: str, request: DispatchRequest) -> OperationResult:
    """Validate and dispatch an approved typed request using a static whitelist."""

    validate_tool_name(tool_name)

    if request.meta.tool_name != tool_name:
        validate_request_model(tool_name, request)

    validate_request_model(tool_name, request)

    handler = _DISPATCH_HANDLERS[tool_name]
    result = handler(request)

    approval = get_approval_requirement(tool_name)
    if result.request_id != request.meta.request_id:
        raise ValueError("Handler returned mismatched request_id.")
    if result.tool_name != tool_name:
        raise ValueError("Handler returned mismatched tool_name.")
    if result.requires_approval != approval.requires_approval:
        raise ValueError("Handler returned mismatched requires_approval.")
    if result.approval_level != approval.approval_level:
        raise ValueError("Handler returned mismatched approval_level.")

    return result
