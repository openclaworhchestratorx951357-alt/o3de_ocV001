from o3de_bridge.approvals import get_approval_requirement
from o3de_bridge.models import (
    ComponentSpec,
    EditorState,
    EntityCreateRequest,
    EntityFindData,
    EntityFindQuery,
    EntityFindResultRecord,
    EntityListData,
    EntityListResultRecord,
    OperationResult,
    ProjectScanData,
    RequestMeta,
    SceneValidationAssetAssignment,
    SceneValidationEntityResult,
    SceneValidateData,
)


def test_request_meta_accepts_approved_shared_fields() -> None:
    meta = RequestMeta(
        request_id="req-1001",
        tool_name="project_scan",
        dry_run=False,
        approval_token=None,
        timestamp="2026-04-01T04:55:00Z",
    )

    assert meta.request_id == "req-1001"
    assert meta.tool_name == "project_scan"
    assert meta.dry_run is False
    assert meta.approval_token is None
    assert meta.timestamp == "2026-04-01T04:55:00Z"


def test_component_spec_accepts_camera_and_mesh() -> None:
    camera = ComponentSpec(type="Camera")
    mesh = ComponentSpec(type="Mesh", asset_hint="Box_1x1.fbx")

    assert camera.type == "Camera"
    assert mesh.type == "Mesh"
    assert mesh.asset_hint == "Box_1x1.fbx"


def test_project_scan_data_uses_typed_editor_state() -> None:
    data = ProjectScanData(
        project_id="McpSandbox",
        project_found=True,
        scenes=["TestLevel01"],
        assets=["Box_1x1.fbx"],
        editor_state=EditorState(running=True),
    )

    assert data.project_found is True
    assert data.editor_state.running is True


def test_scene_validate_data_uses_typed_entity_results() -> None:
    data = SceneValidateData(
        project_id="McpSandbox",
        scene_name="TestLevel01",
        valid=True,
        issues=[],
        entities=[
            SceneValidationEntityResult(
                entity_name="TestBoxEntity",
                exists=True,
                has_camera=True,
                has_mesh=True,
                asset_assignment=SceneValidationAssetAssignment(
                    expected="Box_1x1.fbx",
                    actual="Box_1x1.fbx",
                    matches=True,
                ),
            )
        ],
    )

    assert data.valid is True
    assert len(data.entities) == 1
    assert data.entities[0].asset_assignment is not None
    assert data.entities[0].asset_assignment.matches is True


def test_operation_result_matches_approved_common_shape() -> None:
    result = OperationResult(
        request_id="req-1002",
        tool_name="scene_validate",
        ok=True,
        data=SceneValidateData(
            project_id="McpSandbox",
            scene_name="TestLevel01",
            valid=True,
            issues=[],
            entities=[],
        ),
        warnings=[],
        errors=[],
        logs=[],
        requires_approval=False,
        approval_level="none",
    )

    assert result.ok is True
    assert result.requires_approval is False
    assert result.approval_level == "none"


def test_entity_create_request_uses_typed_component_list() -> None:
    request = EntityCreateRequest(
        meta=RequestMeta(
            request_id="req-1003",
            tool_name="entity_create",
            dry_run=False,
            approval_token="approved-1003",
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_name="TestBoxEntity",
        components=[
            ComponentSpec(type="Camera"),
            ComponentSpec(type="Mesh", asset_hint="Box_1x1.fbx"),
        ],
    )

    assert request.entity_name == "TestBoxEntity"
    assert [component.type for component in request.components] == ["Camera", "Mesh"]


def test_entity_find_data_uses_typed_result_records() -> None:
    query = EntityFindQuery(entity_name="test", match_mode="prefix", limit=10)
    data = EntityFindData(
        project_id="McpSandbox",
        scene_name="TestLevel01",
        match_mode=query.match_mode,
        query_summary="entity_name=test",
        total_matches=2,
        matches=[
            EntityFindResultRecord(
                entity_id="entity-001",
                entity_name="test_entity",
                scene_name="TestLevel01",
                match_reason="entity_name_prefix",
            ),
            EntityFindResultRecord(
                entity_id="entity-002",
                entity_name="test_entity_camera",
                scene_name="TestLevel01",
                match_reason="entity_name_prefix",
            ),
        ],
    )

    assert data.match_mode == "prefix"
    assert data.total_matches == 2
    assert data.matches[0].entity_id == "entity-001"
    assert data.matches[1].entity_name == "test_entity_camera"


def test_entity_list_data_uses_typed_result_records() -> None:
    data = EntityListData(
        project_id="McpSandbox",
        scene_name="TestLevel01",
        scope="scene",
        total_entities=2,
        entities=[
            EntityListResultRecord(
                entity_id="entity-001",
                entity_name="root_entity",
                scene_name="TestLevel01",
                parent_entity_id=None,
                depth=0,
            ),
            EntityListResultRecord(
                entity_id="entity-002",
                entity_name="child_camera",
                scene_name="TestLevel01",
                parent_entity_id="entity-001",
                depth=1,
            ),
        ],
    )

    assert data.scope == "scene"
    assert data.total_entities == 2
    assert data.entities[0].entity_id == "entity-001"
    assert data.entities[1].parent_entity_id == "entity-001"


def test_approval_requirement_matches_expected_tools() -> None:
    assert get_approval_requirement("project_scan").requires_approval is False
    assert get_approval_requirement("scene_validate").requires_approval is False
    assert get_approval_requirement("entity_find").requires_approval is False
    assert get_approval_requirement("entity_list").requires_approval is False
    assert get_approval_requirement("scene_open").requires_approval is True
    assert get_approval_requirement("scene_create").requires_approval is True
    assert get_approval_requirement("entity_create").requires_approval is True
    assert get_approval_requirement("scene_save").requires_approval is True
