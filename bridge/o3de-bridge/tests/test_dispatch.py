import pytest

from o3de_bridge.errors import INVALID_REQUEST, TOOL_NOT_ALLOWED, BridgeValidationError
from o3de_bridge.dispatch import dispatch
from o3de_bridge.models import (
    AssetResolveRequest,
    AssetResolveResponse,
    AssetSearchRequest,
    AssetSearchResponse,
    BridgeHealthRequest,
    BridgeHealthResponse,
    CapabilityEnvelopeData,
    ComponentAddRequest,
    ComponentAddResponse,
    EntityFindQuery,
    EntityFindRequest,
    EntityFindResponse,
    EntityGetRequest,
    EntityListRequest,
    EntityListResponse,
    EntityGetResponse,
    EntityRenameRequest,
    EntityRenameResponse,
    EntitySetTransformRequest,
    EntitySetTransformResponse,
    GetBridgeCapabilitiesRequest,
    GetBridgeCapabilitiesResponse,
    MeshSetModelAssetRequest,
    MeshSetModelAssetResponse,
    ModelAssetTarget,
    ProjectScanRequest,
    RequestMeta,
    SceneOpenRequest,
    TransformMutationPayload,
)


def test_dispatch_project_scan_returns_stubbed_result() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-3001",
            tool_name="project_scan",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    result = dispatch("project_scan", request)

    assert result.request_id == "req-3001"
    assert result.tool_name == "project_scan"
    assert result.ok is True
    assert result.requires_approval is False
    assert result.approval_level == "none"
    assert result.data is not None


def test_dispatch_scene_open_preserves_approval_metadata() -> None:
    request = SceneOpenRequest(
        meta=RequestMeta(
            request_id="req-3002",
            tool_name="scene_open",
            dry_run=False,
            approval_token="approved-3002",
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
    )

    result = dispatch("scene_open", request)

    assert result.request_id == "req-3002"
    assert result.tool_name == "scene_open"
    assert result.requires_approval is True
    assert result.approval_level == "confirm"


def test_dispatch_rejects_unknown_tool_name() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-3003",
            tool_name="project_scan",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("execute_command", request)

    assert exc_info.value.code == TOOL_NOT_ALLOWED
    assert exc_info.value.target == "tool_name"


def test_dispatch_rejects_mismatched_meta_tool_name() -> None:
    request = SceneOpenRequest(
        meta=RequestMeta(
            request_id="req-3004",
            tool_name="scene_create",
            dry_run=False,
            approval_token="approved-3004",
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("scene_open", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "meta.tool_name"


def test_dispatch_get_bridge_capabilities_returns_typed_response() -> None:
    request = GetBridgeCapabilitiesRequest(
        meta=RequestMeta(
            request_id="req-3005",
            tool_name="get_bridge_capabilities",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T03:00:00Z",
        ),
        project_id="McpSandbox",
    )

    result = dispatch("get_bridge_capabilities", request)

    assert isinstance(result, GetBridgeCapabilitiesResponse)
    assert result.request_id == "req-3005"
    assert result.tool_name == "get_bridge_capabilities"
    assert isinstance(result.data, CapabilityEnvelopeData)
    assert result.data.bridge_capabilities.supported_domains.domains[0].domain_name == "core lifecycle"
    assert result.data.bridge_capabilities.supported_components.components[0].mutation_safety_class == "scoped_mutation"
    assert result.data.bridge_capabilities.mutation_safety_classes.classes[0].class_name == "read_only"
    assert "get_bridge_capabilities" in result.logs[0].message
    assert result.requires_approval is False
    assert result.approval_level == "none"


def test_dispatch_get_bridge_capabilities_rejects_invalid_request_shape() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-3006",
            tool_name="get_bridge_capabilities",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("get_bridge_capabilities", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "request_model"


def test_dispatch_bridge_health_returns_typed_health_response() -> None:
    request = BridgeHealthRequest(
        meta=RequestMeta(
            request_id="req-3007",
            tool_name="bridge_health",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T03:01:00Z",
        ),
        project_id="McpSandbox",
    )

    result = dispatch("bridge_health", request)

    assert isinstance(result, BridgeHealthResponse)
    assert result.tool_name == "bridge_health"
    assert result.ok is True
    assert result.data.bridge_version == "1.0.0"
    assert result.data.transport_ready is True
    assert result.data.bootstrap_installed is False
    assert result.data.live_session_connected is False
    assert "get_bridge_capabilities" in result.data.registered_handlers
    assert "bridge_health" in result.data.registered_handlers
    assert result.data.registered_handlers == sorted(result.data.registered_handlers)


def test_dispatch_bridge_health_rejects_invalid_request_shape() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-3008",
            tool_name="bridge_health",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("bridge_health", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "request_model"


def test_dispatch_entity_get_returns_typed_response() -> None:
    request = EntityGetRequest(
        meta=RequestMeta(
            request_id="req-3009",
            tool_name="entity_get",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T03:31:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
    )

    result = dispatch("entity_get", request)

    assert isinstance(result, EntityGetResponse)
    assert result.request_id == "req-3009"
    assert result.tool_name == "entity_get"
    assert result.data.entity.entity_id == "entity-123"
    assert result.data.entity.entity_name == "stub_entity"
    assert result.data.entity.scene_name == "TestLevel01"
    assert result.data.entity.exists is False


def test_dispatch_entity_get_rejects_invalid_request_shape() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-3010",
            tool_name="entity_get",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("entity_get", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "request_model"


def test_dispatch_entity_get_rejects_missing_entity_id() -> None:
    with pytest.raises(ValueError):
        EntityGetRequest(
            meta=RequestMeta(
                request_id="req-3011",
                tool_name="entity_get",
                dry_run=False,
                approval_token=None,
                timestamp=None,
            ),
            project_id="McpSandbox",
            scene_name="TestLevel01",
            entity_id="",
        )


def test_dispatch_entity_find_returns_typed_response_for_name_query() -> None:
    request = EntityFindRequest(
        meta=RequestMeta(
            request_id="req-3012",
            tool_name="entity_find",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T03:33:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        query=EntityFindQuery(entity_name="test", match_mode="prefix", limit=10),
    )

    result = dispatch("entity_find", request)

    assert isinstance(result, EntityFindResponse)
    assert result.tool_name == "entity_find"
    assert result.data.match_mode == "prefix"
    assert result.data.total_matches == 2
    assert result.data.matches[0].entity_id == "entity-001"
    assert result.data.matches[0].entity_name == "test_entity"
    assert result.data.matches[1].entity_id == "entity-002"
    assert result.requires_approval is False
    assert result.approval_level == "none"


def test_dispatch_entity_find_returns_typed_response_for_entity_id_query() -> None:
    request = EntityFindRequest(
        meta=RequestMeta(
            request_id="req-3013",
            tool_name="entity_find",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T03:34:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        query=EntityFindQuery(entity_name=None, entity_id="entity-123", match_mode="contains", limit=5),
    )

    result = dispatch("entity_find", request)

    assert isinstance(result, EntityFindResponse)
    assert result.tool_name == "entity_find"
    assert result.data.query_summary == "entity_id=entity-123"
    assert result.data.total_matches == 1
    assert result.data.matches[0].entity_id == "entity-123"
    assert result.data.matches[0].match_reason == "entity_id_exact"


def test_dispatch_entity_find_rejects_invalid_request_shape() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-3014",
            tool_name="entity_find",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("entity_find", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "request_model"


def test_dispatch_entity_list_returns_typed_response_for_scene_scope() -> None:
    request = EntityListRequest(
        meta=RequestMeta(
            request_id="req-3019",
            tool_name="entity_list",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T08:40:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        scope="scene",
        limit=10,
    )

    result = dispatch("entity_list", request)

    assert isinstance(result, EntityListResponse)
    assert result.tool_name == "entity_list"
    assert result.data.scope == "scene"
    assert result.data.total_entities == 3
    assert result.data.entities[0].entity_id == "entity-001"
    assert result.data.entities[1].parent_entity_id == "entity-001"
    assert result.requires_approval is False
    assert result.approval_level == "none"


def test_dispatch_entity_list_returns_typed_response_for_root_scope() -> None:
    request = EntityListRequest(
        meta=RequestMeta(
            request_id="req-3020",
            tool_name="entity_list",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T08:41:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        scope="root_only",
        limit=10,
    )

    result = dispatch("entity_list", request)

    assert isinstance(result, EntityListResponse)
    assert result.tool_name == "entity_list"
    assert result.data.scope == "root_only"
    assert result.data.total_entities == 1
    assert result.data.entities[0].depth == 0


def test_dispatch_entity_list_rejects_invalid_request_shape() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-3021",
            tool_name="entity_list",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("entity_list", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "request_model"


def test_dispatch_asset_search_returns_typed_response() -> None:
    request = AssetSearchRequest(
        meta=RequestMeta(
            request_id="req-3022",
            tool_name="asset_search",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T03:35:00Z",
        ),
        project_id="McpSandbox",
        query="box",
        asset_category="model",
        limit=5,
    )

    result = dispatch("asset_search", request)

    assert isinstance(result, AssetSearchResponse)
    assert result.tool_name == "asset_search"
    assert result.data.matches[0].asset_id == "asset-001"
    assert result.data.matches[0].asset_path == "objects/_primitives/_box_1x1.fbx.azmodel"
    assert result.data.matches[0].asset_category == "model"
    assert result.data.matches[0].resolved is True


def test_dispatch_asset_resolve_returns_typed_response() -> None:
    request = AssetResolveRequest(
        meta=RequestMeta(
            request_id="req-3023",
            tool_name="asset_resolve",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T03:34:00Z",
        ),
        project_id="McpSandbox",
        asset_id="asset-001",
        asset_hint=None,
    )

    result = dispatch("asset_resolve", request)

    assert isinstance(result, AssetResolveResponse)
    assert result.tool_name == "asset_resolve"
    assert result.data.asset is not None
    assert result.data.asset.asset_id == "asset-001"
    assert result.data.asset.asset_category == "model"
    assert result.data.resolution_status == "resolved"


def test_dispatch_asset_search_rejects_invalid_request_shape() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-3024",
            tool_name="asset_search",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("asset_search", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "request_model"


def test_dispatch_asset_resolve_rejects_invalid_request_shape() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-3025",
            tool_name="asset_resolve",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("asset_resolve", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "request_model"


def test_dispatch_component_add_returns_fail_closed_typed_response() -> None:
    request = ComponentAddRequest(
        meta=RequestMeta(
            request_id="req-3016",
            tool_name="component_add",
            dry_run=False,
            approval_token="approved-3016",
            timestamp="2026-04-04T03:40:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        component_type="Camera",
        component_config=None,
    )

    result = dispatch("component_add", request)

    assert isinstance(result, ComponentAddResponse)
    assert result.tool_name == "component_add"
    assert result.data.entity_id == "entity-123"
    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.added_component is not None
    assert result.data.added_component.added is False
    assert result.data.added_component.approval_required is True


def test_dispatch_component_add_rejects_invalid_request_shape() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-3017",
            tool_name="component_add",
            dry_run=False,
            approval_token="approved-3017",
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("component_add", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "request_model"


def test_component_add_request_rejects_missing_entity_id() -> None:
    with pytest.raises(ValueError):
        ComponentAddRequest(
            meta=RequestMeta(
                request_id="req-3018",
                tool_name="component_add",
                dry_run=False,
                approval_token="approved-3018",
                timestamp=None,
            ),
            project_id="McpSandbox",
            scene_name="TestLevel01",
            entity_id="",
            component_type="Camera",
            component_config=None,
        )


def test_dispatch_component_add_rejects_disallowed_component_type() -> None:
    request = ComponentAddRequest(
        meta=RequestMeta(
            request_id="req-3019",
            tool_name="component_add",
            dry_run=False,
            approval_token="approved-3019",
            timestamp="2026-04-04T03:41:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        component_type="ScriptCanvas",
        component_config=None,
    )

    result = dispatch("component_add", request)

    assert isinstance(result, ComponentAddResponse)
    assert result.data.outcome_status == "rejected_disallowed_component_type"
    assert result.data.added_component is not None
    assert result.data.added_component.added is False
    assert result.data.added_component.approval_required is True


def test_component_add_request_rejects_missing_component_type() -> None:
    with pytest.raises(ValueError):
        ComponentAddRequest(
            meta=RequestMeta(
                request_id="req-3020",
                tool_name="component_add",
                dry_run=False,
                approval_token="approved-3020",
                timestamp=None,
            ),
            project_id="McpSandbox",
            scene_name="TestLevel01",
            entity_id="entity-123",
            component_type="",
            component_config=None,
        )


def test_dispatch_component_add_rejects_missing_approval_token() -> None:
    request = ComponentAddRequest(
        meta=RequestMeta(
            request_id="req-3021",
            tool_name="component_add",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T03:42:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        component_type="Camera",
        component_config=None,
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("component_add", request)

    assert exc_info.value.code == "approval_required"
    assert exc_info.value.target == "approval_token"


def test_dispatch_component_add_preserves_fail_closed_typed_shape() -> None:
    request = ComponentAddRequest(
        meta=RequestMeta(
            request_id="req-3022",
            tool_name="component_add",
            dry_run=False,
            approval_token="approved-3022",
            timestamp="2026-04-04T03:43:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        component_type="Mesh",
        component_config=None,
    )

    result = dispatch("component_add", request)

    assert isinstance(result, ComponentAddResponse)
    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.added_component is not None
    assert result.data.added_component.component_type == "Mesh"
    assert result.data.added_component.approval_required is True


def test_dispatch_entity_rename_returns_fail_closed_typed_response() -> None:
    request = EntityRenameRequest(
        meta=RequestMeta(
            request_id="req-3023",
            tool_name="entity_rename",
            dry_run=False,
            approval_token="approved-3023",
            timestamp="2026-04-04T03:50:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        current_name="old_name",
        new_name="new_name",
    )

    result = dispatch("entity_rename", request)

    assert isinstance(result, EntityRenameResponse)
    assert result.tool_name == "entity_rename"
    assert result.data.entity_id == "entity-123"
    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.renamed_entity is not None
    assert result.data.renamed_entity.renamed is False
    assert result.data.renamed_entity.approval_required is True


def test_dispatch_entity_rename_rejects_invalid_request_shape() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-3024",
            tool_name="entity_rename",
            dry_run=False,
            approval_token="approved-3024",
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("entity_rename", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "request_model"


def test_entity_rename_request_rejects_missing_new_name() -> None:
    with pytest.raises(ValueError):
        EntityRenameRequest(
            meta=RequestMeta(
                request_id="req-3025",
                tool_name="entity_rename",
                dry_run=False,
                approval_token="approved-3025",
                timestamp=None,
            ),
            project_id="McpSandbox",
            scene_name="TestLevel01",
            entity_id="entity-123",
            current_name="old_name",
            new_name="",
        )


def test_dispatch_entity_rename_rejects_invalid_rename_attempt() -> None:
    request = EntityRenameRequest(
        meta=RequestMeta(
            request_id="req-3026",
            tool_name="entity_rename",
            dry_run=False,
            approval_token="approved-3026",
            timestamp="2026-04-04T03:51:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        current_name="same_name",
        new_name="same_name",
    )

    result = dispatch("entity_rename", request)

    assert isinstance(result, EntityRenameResponse)
    assert result.data.outcome_status == "rejected_invalid_rename"
    assert result.data.renamed_entity is not None
    assert result.data.renamed_entity.renamed is False


def test_entity_rename_request_rejects_missing_entity_id() -> None:
    with pytest.raises(ValueError):
        EntityRenameRequest(
            meta=RequestMeta(
                request_id="req-3027",
                tool_name="entity_rename",
                dry_run=False,
                approval_token="approved-3027",
                timestamp=None,
            ),
            project_id="McpSandbox",
            scene_name="TestLevel01",
            entity_id="",
            current_name="old_name",
            new_name="new_name",
        )


def test_dispatch_entity_rename_rejects_missing_approval_token() -> None:
    request = EntityRenameRequest(
        meta=RequestMeta(
            request_id="req-3028",
            tool_name="entity_rename",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T03:52:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        current_name="old_name",
        new_name="new_name",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("entity_rename", request)

    assert exc_info.value.code == "approval_required"
    assert exc_info.value.target == "approval_token"


def test_dispatch_entity_rename_preserves_fail_closed_typed_shape() -> None:
    request = EntityRenameRequest(
        meta=RequestMeta(
            request_id="req-3029",
            tool_name="entity_rename",
            dry_run=False,
            approval_token="approved-3029",
            timestamp="2026-04-04T03:53:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        current_name="old_name",
        new_name="new_name_2",
    )

    result = dispatch("entity_rename", request)

    assert isinstance(result, EntityRenameResponse)
    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.renamed_entity is not None
    assert result.data.renamed_entity.entity_id == "entity-123"
    assert result.data.renamed_entity.approval_required is True


def test_dispatch_entity_set_transform_returns_fail_closed_typed_response() -> None:
    request = EntitySetTransformRequest(
        meta=RequestMeta(
            request_id="req-3030",
            tool_name="entity_set_transform",
            dry_run=False,
            approval_token="approved-3030",
            timestamp="2026-04-04T04:01:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        transform=TransformMutationPayload(
            translation=(1.0, 2.0, 3.0),
            rotation_euler_degrees=None,
            scale=None,
        ),
    )

    result = dispatch("entity_set_transform", request)

    assert isinstance(result, EntitySetTransformResponse)
    assert result.tool_name == "entity_set_transform"
    assert result.data.entity_id == "entity-123"
    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.applied_transform is not None
    assert result.data.applied_transform.applied is False
    assert result.data.applied_transform.approval_required is True


def test_dispatch_entity_set_transform_rejects_invalid_request_shape() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-3031",
            tool_name="entity_set_transform",
            dry_run=False,
            approval_token="approved-3031",
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("entity_set_transform", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "request_model"


def test_entity_set_transform_request_rejects_missing_transform_input() -> None:
    request = EntitySetTransformRequest(
        meta=RequestMeta(
            request_id="req-3032",
            tool_name="entity_set_transform",
            dry_run=False,
            approval_token="approved-3032",
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        transform=TransformMutationPayload(
            translation=None,
            rotation_euler_degrees=None,
            scale=None,
        ),
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("entity_set_transform", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "transform"


def test_dispatch_entity_set_transform_rejects_invalid_transform_attempt() -> None:
    request = EntitySetTransformRequest(
        meta=RequestMeta(
            request_id="req-3033",
            tool_name="entity_set_transform",
            dry_run=False,
            approval_token="approved-3033",
            timestamp="2026-04-04T04:02:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        transform=TransformMutationPayload(
            translation=(0.0, 0.0, 0.0),
            rotation_euler_degrees=None,
            scale=None,
        ),
    )

    result = dispatch("entity_set_transform", request)

    assert isinstance(result, EntitySetTransformResponse)
    assert result.data.outcome_status == "rejected_invalid_transform"
    assert result.data.applied_transform is not None
    assert result.data.applied_transform.applied is False


def test_entity_set_transform_request_rejects_missing_entity_id() -> None:
    with pytest.raises(ValueError):
        EntitySetTransformRequest(
            meta=RequestMeta(
                request_id="req-3034",
                tool_name="entity_set_transform",
                dry_run=False,
                approval_token="approved-3034",
                timestamp=None,
            ),
            project_id="McpSandbox",
            scene_name="TestLevel01",
            entity_id="",
            transform=TransformMutationPayload(
                translation=(1.0, 2.0, 3.0),
                rotation_euler_degrees=None,
                scale=None,
            ),
        )


def test_dispatch_entity_set_transform_rejects_missing_approval_token() -> None:
    request = EntitySetTransformRequest(
        meta=RequestMeta(
            request_id="req-3035",
            tool_name="entity_set_transform",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T04:03:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        transform=TransformMutationPayload(
            translation=(1.0, 2.0, 3.0),
            rotation_euler_degrees=None,
            scale=None,
        ),
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("entity_set_transform", request)

    assert exc_info.value.code == "approval_required"
    assert exc_info.value.target == "approval_token"


def test_dispatch_entity_set_transform_preserves_fail_closed_typed_shape() -> None:
    request = EntitySetTransformRequest(
        meta=RequestMeta(
            request_id="req-3036",
            tool_name="entity_set_transform",
            dry_run=False,
            approval_token="approved-3036",
            timestamp="2026-04-04T04:04:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        transform=TransformMutationPayload(
            translation=(4.0, 5.0, 6.0),
            rotation_euler_degrees=None,
            scale=None,
        ),
    )

    result = dispatch("entity_set_transform", request)

    assert isinstance(result, EntitySetTransformResponse)
    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.applied_transform is not None
    assert result.data.applied_transform.entity_id == "entity-123"
    assert result.data.applied_transform.approval_required is True


def test_dispatch_mesh_set_model_asset_returns_fail_closed_typed_response() -> None:
    request = MeshSetModelAssetRequest(
        meta=RequestMeta(
            request_id="req-3037",
            tool_name="mesh_set_model_asset",
            dry_run=False,
            approval_token="approved-3037",
            timestamp="2026-04-04T06:48:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        model_asset=ModelAssetTarget(model_asset_path="objects/_primitives/_box_1x1.fbx.azmodel"),
    )

    result = dispatch("mesh_set_model_asset", request)

    assert isinstance(result, MeshSetModelAssetResponse)
    assert result.tool_name == "mesh_set_model_asset"
    assert result.data.entity_id == "entity-123"
    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.assigned_model_asset is not None
    assert result.data.assigned_model_asset.assigned is False
    assert result.data.assigned_model_asset.approval_required is True


def test_mesh_set_model_asset_request_rejects_missing_entity_id() -> None:
    with pytest.raises(ValueError):
        MeshSetModelAssetRequest(
            meta=RequestMeta(
                request_id="req-3038",
                tool_name="mesh_set_model_asset",
                dry_run=False,
                approval_token="approved-3038",
                timestamp=None,
            ),
            project_id="McpSandbox",
            scene_name="TestLevel01",
            entity_id="",
            model_asset=ModelAssetTarget(model_asset_path="objects/_primitives/_box_1x1.fbx.azmodel"),
        )


def test_dispatch_mesh_set_model_asset_rejects_invalid_model_asset_attempt() -> None:
    request = MeshSetModelAssetRequest(
        meta=RequestMeta(
            request_id="req-3039",
            tool_name="mesh_set_model_asset",
            dry_run=False,
            approval_token="approved-3039",
            timestamp="2026-04-04T06:49:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        model_asset=ModelAssetTarget(model_asset_path="textures/not-a-model.txt"),
    )

    result = dispatch("mesh_set_model_asset", request)

    assert isinstance(result, MeshSetModelAssetResponse)
    assert result.data.outcome_status == "rejected_disallowed_model_asset"
    assert result.data.assigned_model_asset is not None
    assert result.data.assigned_model_asset.assigned is False


def test_dispatch_mesh_set_model_asset_preserves_fail_closed_typed_shape() -> None:
    request = MeshSetModelAssetRequest(
        meta=RequestMeta(
            request_id="req-3040",
            tool_name="mesh_set_model_asset",
            dry_run=False,
            approval_token="approved-3040",
            timestamp="2026-04-04T06:50:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        model_asset=ModelAssetTarget(model_asset_path="objects/_primitives/_box_1x1.fbx.azmodel"),
    )

    result = dispatch("mesh_set_model_asset", request)

    assert isinstance(result, MeshSetModelAssetResponse)
    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.assigned_model_asset is not None
    assert result.data.assigned_model_asset.entity_id == "entity-123"
    assert result.data.assigned_model_asset.model_asset.model_asset_path == "objects/_primitives/_box_1x1.fbx.azmodel"
    assert result.data.assigned_model_asset.approval_required is True


def test_dispatch_mesh_set_model_asset_rejects_missing_approval_token() -> None:
    request = MeshSetModelAssetRequest(
        meta=RequestMeta(
            request_id="req-3041",
            tool_name="mesh_set_model_asset",
            dry_run=False,
            approval_token=None,
            timestamp="2026-04-04T06:51:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        model_asset=ModelAssetTarget(model_asset_path="objects/_primitives/_box_1x1.fbx.azmodel"),
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        dispatch("mesh_set_model_asset", request)

    assert exc_info.value.code == "approval_required"
    assert exc_info.value.target == "approval_token"


def test_mesh_set_model_asset_request_rejects_missing_model_asset_target_input() -> None:
    with pytest.raises(ValueError):
        MeshSetModelAssetRequest(
            meta=RequestMeta(
                request_id="req-3042",
                tool_name="mesh_set_model_asset",
                dry_run=False,
                approval_token="approved-3042",
                timestamp=None,
            ),
            project_id="McpSandbox",
            scene_name="TestLevel01",
            entity_id="entity-123",
            model_asset=ModelAssetTarget(model_asset_path=""),
        )


def test_dispatch_mesh_set_model_asset_preserves_fail_closed_outcome_status() -> None:
    request = MeshSetModelAssetRequest(
        meta=RequestMeta(
            request_id="req-3043",
            tool_name="mesh_set_model_asset",
            dry_run=False,
            approval_token="approved-3043",
            timestamp="2026-04-04T06:52:00Z",
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_id="entity-123",
        model_asset=ModelAssetTarget(model_asset_path="objects/_primitives/_box_1x1.fbx.azmodel"),
    )

    result = dispatch("mesh_set_model_asset", request)

    assert isinstance(result, MeshSetModelAssetResponse)
    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.assigned_model_asset is not None
    assert result.data.assigned_model_asset.approval_required is True
