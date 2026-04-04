from o3de_bridge.errors import BridgeValidationError
from o3de_bridge.models import (
    BridgeHealthResponse,
    GetBridgeCapabilitiesResponse,
    MeshSetModelAssetResponse,
)
from o3de_mcp_server.server import (
    EXPOSED_TOOL_NAMES,
    ServerExposureError,
    handle_tool_call,
    list_exposed_tools,
)


def test_handle_tool_call_returns_get_bridge_capabilities_response() -> None:
    result = handle_tool_call(
        "get_bridge_capabilities",
        {
            "meta": {
                "request_id": "req-server-5001",
                "tool_name": "get_bridge_capabilities",
                "dry_run": False,
                "approval_token": None,
                "timestamp": "2026-04-04T03:20:00Z",
            },
            "project_id": "McpSandbox",
        },
    )

    assert isinstance(result, GetBridgeCapabilitiesResponse)
    assert result.tool_name == "get_bridge_capabilities"


def test_handle_tool_call_returns_bridge_health_response() -> None:
    result = handle_tool_call(
        "bridge_health",
        {
            "meta": {
                "request_id": "req-server-5002",
                "tool_name": "bridge_health",
                "dry_run": False,
                "approval_token": None,
                "timestamp": "2026-04-04T03:21:00Z",
            }
        },
    )

    assert isinstance(result, BridgeHealthResponse)
    assert result.tool_name == "bridge_health"


def test_handle_tool_call_rejects_non_exposed_tool() -> None:
    try:
        handle_tool_call("entity_create", {})
    except ServerExposureError as exc:
        assert exc.args == ("entity_create",)
    else:
        raise AssertionError("Expected ServerExposureError")


def test_handle_tool_call_routes_project_scan() -> None:
    result = handle_tool_call(
        "project_scan",
        {
            "meta": {
                "request_id": "req-server-5003",
                "tool_name": "project_scan",
                "dry_run": False,
                "approval_token": None,
                "timestamp": "2026-04-04T03:22:00Z",
            },
            "project_id": "McpSandbox",
        },
    )

    assert result.tool_name == "project_scan"
    assert result.request_id == "req-server-5003"


def test_handle_tool_call_routes_scene_open() -> None:
    result = handle_tool_call(
        "scene_open",
        {
            "meta": {
                "request_id": "req-server-5004",
                "tool_name": "scene_open",
                "dry_run": False,
                "approval_token": "approved-5004",
                "timestamp": "2026-04-04T03:23:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
        },
    )

    assert result.tool_name == "scene_open"
    assert result.request_id == "req-server-5004"


def test_handle_tool_call_routes_scene_create() -> None:
    result = handle_tool_call(
        "scene_create",
        {
            "meta": {
                "request_id": "req-server-5005",
                "tool_name": "scene_create",
                "dry_run": False,
                "approval_token": "approved-5005",
                "timestamp": "2026-04-04T03:24:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "NewScene02",
            "template": "Prefabs/Default_Level.prefab",
        },
    )

    assert result.tool_name == "scene_create"
    assert result.request_id == "req-server-5005"


def test_handle_tool_call_routes_scene_save() -> None:
    result = handle_tool_call(
        "scene_save",
        {
            "meta": {
                "request_id": "req-server-5006",
                "tool_name": "scene_save",
                "dry_run": False,
                "approval_token": "approved-5006",
                "timestamp": "2026-04-04T03:28:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
        },
    )

    assert result.tool_name == "scene_save"
    assert result.request_id == "req-server-5006"


def test_handle_tool_call_routes_scene_validate() -> None:
    result = handle_tool_call(
        "scene_validate",
        {
            "meta": {
                "request_id": "req-server-5007",
                "tool_name": "scene_validate",
                "dry_run": False,
                "approval_token": None,
                "timestamp": "2026-04-04T03:29:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
            "expected_entities": [],
        },
    )

    assert result.tool_name == "scene_validate"
    assert result.request_id == "req-server-5007"


def test_handle_tool_call_routes_entity_create() -> None:
    result = handle_tool_call(
        "entity_create",
        {
            "meta": {
                "request_id": "req-server-5008",
                "tool_name": "entity_create",
                "dry_run": False,
                "approval_token": "approved-5008",
                "timestamp": "2026-04-04T03:30:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
            "entity_name": "bridge_entity_03",
            "components": [],
        },
    )

    assert result.tool_name == "entity_create"
    assert result.request_id == "req-server-5008"


def test_handle_tool_call_routes_entity_get() -> None:
    result = handle_tool_call(
        "entity_get",
        {
            "meta": {
                "request_id": "req-server-5009",
                "tool_name": "entity_get",
                "dry_run": False,
                "approval_token": None,
                "timestamp": "2026-04-04T03:32:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
            "entity_id": "entity-123",
        },
    )

    assert result.tool_name == "entity_get"
    assert result.request_id == "req-server-5009"
    assert result.data.entity.entity_id == "entity-123"


def test_handle_tool_call_routes_entity_find() -> None:
    result = handle_tool_call(
        "entity_find",
        {
            "meta": {
                "request_id": "req-server-5010",
                "tool_name": "entity_find",
                "dry_run": False,
                "approval_token": None,
                "timestamp": "2026-04-04T08:12:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
            "query": {
                "entity_name": "bridge",
                "entity_id": None,
                "match_mode": "contains",
                "limit": 10,
            },
        },
    )

    assert result.tool_name == "entity_find"
    assert result.request_id == "req-server-5010"
    assert result.data.total_matches == 1
    assert result.data.matches[0].entity_id == "entity-003"


def test_handle_tool_call_routes_asset_search() -> None:
    result = handle_tool_call(
        "asset_search",
        {
            "meta": {
                "request_id": "req-server-5011",
                "tool_name": "asset_search",
                "dry_run": False,
                "approval_token": None,
                "timestamp": "2026-04-04T03:37:00Z",
            },
            "project_id": "McpSandbox",
            "query": "box",
            "asset_category": "model",
            "limit": 5,
        },
    )

    assert result.tool_name == "asset_search"
    assert result.request_id == "req-server-5011"
    assert result.data.matches[0].asset_id == "asset-001"


def test_handle_tool_call_routes_asset_resolve() -> None:
    result = handle_tool_call(
        "asset_resolve",
        {
            "meta": {
                "request_id": "req-server-5012",
                "tool_name": "asset_resolve",
                "dry_run": False,
                "approval_token": None,
                "timestamp": "2026-04-04T03:38:00Z",
            },
            "project_id": "McpSandbox",
            "asset_id": "asset-001",
            "asset_hint": None,
        },
    )

    assert result.tool_name == "asset_resolve"
    assert result.request_id == "req-server-5012"
    assert result.data.asset is not None
    assert result.data.asset.asset_id == "asset-001"


def test_handle_tool_call_routes_component_add() -> None:
    result = handle_tool_call(
        "component_add",
        {
            "meta": {
                "request_id": "req-server-5012",
                "tool_name": "component_add",
                "dry_run": False,
                "approval_token": "approved-5012",
                "timestamp": "2026-04-04T03:48:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
            "entity_id": "entity-123",
            "component_type": "Camera",
            "component_config": None,
        },
    )

    assert result.tool_name == "component_add"
    assert result.request_id == "req-server-5012"
    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.added_component is not None
    assert result.data.added_component.approval_required is True


def test_handle_tool_call_component_add_preserves_fail_closed_shape() -> None:
    result = handle_tool_call(
        "component_add",
        {
            "meta": {
                "request_id": "req-server-5013",
                "tool_name": "component_add",
                "dry_run": False,
                "approval_token": "approved-5013",
                "timestamp": "2026-04-04T03:49:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
            "entity_id": "entity-123",
            "component_type": "Mesh",
            "component_config": None,
        },
    )

    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.added_component is not None
    assert result.data.added_component.added is False
    assert result.data.added_component.component_type == "Mesh"


def test_handle_tool_call_routes_entity_rename() -> None:
    result = handle_tool_call(
        "entity_rename",
        {
            "meta": {
                "request_id": "req-server-5014",
                "tool_name": "entity_rename",
                "dry_run": False,
                "approval_token": "approved-5014",
                "timestamp": "2026-04-04T03:59:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
            "entity_id": "entity-123",
            "current_name": "old_name",
            "new_name": "new_name",
        },
    )

    assert result.tool_name == "entity_rename"
    assert result.request_id == "req-server-5014"
    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.renamed_entity is not None
    assert result.data.renamed_entity.approval_required is True


def test_handle_tool_call_entity_rename_preserves_fail_closed_shape() -> None:
    result = handle_tool_call(
        "entity_rename",
        {
            "meta": {
                "request_id": "req-server-5015",
                "tool_name": "entity_rename",
                "dry_run": False,
                "approval_token": "approved-5015",
                "timestamp": "2026-04-04T04:00:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
            "entity_id": "entity-123",
            "current_name": "old_name",
            "new_name": "new_name_2",
        },
    )

    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.renamed_entity is not None
    assert result.data.renamed_entity.entity_id == "entity-123"
    assert result.data.renamed_entity.renamed is False


def test_handle_tool_call_routes_entity_set_transform() -> None:
    result = handle_tool_call(
        "entity_set_transform",
        {
            "meta": {
                "request_id": "req-server-5016",
                "tool_name": "entity_set_transform",
                "dry_run": False,
                "approval_token": "approved-5016",
                "timestamp": "2026-04-04T04:09:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
            "entity_id": "entity-123",
            "transform": {
                "translation": [1.0, 2.0, 3.0],
                "rotation_euler_degrees": None,
                "scale": None,
            },
        },
    )

    assert result.tool_name == "entity_set_transform"
    assert result.request_id == "req-server-5016"
    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.applied_transform is not None
    assert result.data.applied_transform.approval_required is True


def test_handle_tool_call_entity_set_transform_preserves_fail_closed_shape() -> None:
    result = handle_tool_call(
        "entity_set_transform",
        {
            "meta": {
                "request_id": "req-server-5017",
                "tool_name": "entity_set_transform",
                "dry_run": False,
                "approval_token": "approved-5017",
                "timestamp": "2026-04-04T04:10:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
            "entity_id": "entity-123",
            "transform": {
                "translation": [4.0, 5.0, 6.0],
                "rotation_euler_degrees": None,
                "scale": None,
            },
        },
    )

    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.applied_transform is not None
    assert result.data.applied_transform.entity_id == "entity-123"
    assert result.data.applied_transform.applied is False


def test_handle_tool_call_entity_set_transform_rejects_missing_approval_token() -> None:
    try:
        handle_tool_call(
            "entity_set_transform",
            {
                "meta": {
                    "request_id": "req-server-5018",
                    "tool_name": "entity_set_transform",
                    "dry_run": False,
                    "approval_token": None,
                    "timestamp": "2026-04-04T04:11:00Z",
                },
                "project_id": "McpSandbox",
                "scene_name": "TestLevel01",
                "entity_id": "entity-123",
                "transform": {
                    "translation": [1.0, 2.0, 3.0],
                    "rotation_euler_degrees": None,
                    "scale": None,
                },
            },
        )
    except BridgeValidationError as exc:
        assert exc.code == "approval_required"
        assert exc.target == "approval_token"
    else:
        raise AssertionError("Expected BridgeValidationError")


def test_handle_tool_call_routes_mesh_set_model_asset() -> None:
    result = handle_tool_call(
        "mesh_set_model_asset",
        {
            "meta": {
                "request_id": "req-server-5019",
                "tool_name": "mesh_set_model_asset",
                "dry_run": False,
                "approval_token": "approved-5019",
                "timestamp": "2026-04-04T06:58:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
            "entity_id": "entity-123",
            "model_asset": {
                "model_asset_path": "objects/_primitives/_box_1x1.fbx.azmodel",
                "asset_category": "model",
            },
        },
    )

    assert isinstance(result, MeshSetModelAssetResponse)
    assert result.tool_name == "mesh_set_model_asset"
    assert result.request_id == "req-server-5019"
    assert result.data.outcome_status == "rejected_unapproved_mutation"


def test_handle_tool_call_mesh_set_model_asset_preserves_fail_closed_shape() -> None:
    result = handle_tool_call(
        "mesh_set_model_asset",
        {
            "meta": {
                "request_id": "req-server-5020",
                "tool_name": "mesh_set_model_asset",
                "dry_run": False,
                "approval_token": "approved-5020",
                "timestamp": "2026-04-04T06:59:00Z",
            },
            "project_id": "McpSandbox",
            "scene_name": "TestLevel01",
            "entity_id": "entity-123",
            "model_asset": {
                "model_asset_path": "objects/_primitives/_box_1x1.fbx.azmodel",
                "asset_category": "model",
            },
        },
    )

    assert result.data.outcome_status == "rejected_unapproved_mutation"
    assert result.data.assigned_model_asset is not None
    assert result.data.assigned_model_asset.entity_id == "entity-123"
    assert result.data.assigned_model_asset.assigned is False
    assert result.data.assigned_model_asset.approval_required is True


def test_handle_tool_call_mesh_set_model_asset_rejects_missing_approval_token() -> None:
    try:
        handle_tool_call(
            "mesh_set_model_asset",
            {
                "meta": {
                    "request_id": "req-server-5021",
                    "tool_name": "mesh_set_model_asset",
                    "dry_run": False,
                    "approval_token": None,
                    "timestamp": "2026-04-04T07:00:00Z",
                },
                "project_id": "McpSandbox",
                "scene_name": "TestLevel01",
                "entity_id": "entity-123",
                "model_asset": {
                    "model_asset_path": "objects/_primitives/_box_1x1.fbx.azmodel",
                    "asset_category": "model",
                },
            },
        )
    except BridgeValidationError as exc:
        assert exc.code == "approval_required"
        assert exc.target == "approval_token"
    else:
        raise AssertionError("Expected BridgeValidationError")


def test_server_exposure_boundary_is_limited_to_current_approved_set() -> None:
    assert EXPOSED_TOOL_NAMES == (
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
    assert list_exposed_tools() == (
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
