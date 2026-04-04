import pytest

from o3de_bridge.errors import (
    APPROVAL_REQUIRED,
    INVALID_COMPONENT,
    INVALID_ENTITY_NAME,
    INVALID_PROJECT_ID,
    INVALID_REQUEST,
    INVALID_SCENE_NAME,
    TOOL_NOT_ALLOWED,
    BridgeValidationError,
)
from o3de_bridge.models import (
    ComponentSpec,
    EntityAncestorsRequest,
    EntityChildrenRequest,
    EntityCreateRequest,
    EntityFindQuery,
    EntityParentRequest,
    EntityFindRequest,
    EntityListRequest,
    ProjectScanRequest,
    RequestMeta,
    SceneOpenRequest,
)
from o3de_bridge.validators import (
    validate_component_specs,
    validate_entity_name,
    validate_project_id,
    validate_request_meta,
    validate_request_model,
    validate_scene_name,
    validate_tool_name,
)


def test_validate_tool_name_accepts_only_approved_tools() -> None:
    for tool_name in (
        "project_scan",
        "scene_open",
        "scene_create",
        "entity_create",
        "scene_save",
        "scene_validate",
    ):
        validate_tool_name(tool_name)


def test_validate_tool_name_rejects_unknown_tool() -> None:
    with pytest.raises(BridgeValidationError) as exc_info:
        validate_tool_name("execute_command")

    assert exc_info.value.code == TOOL_NOT_ALLOWED
    assert exc_info.value.target == "tool_name"


def test_validate_request_meta_accepts_valid_meta() -> None:
    meta = RequestMeta(
        request_id="req-2001",
        tool_name="project_scan",
        dry_run=False,
        approval_token=None,
        timestamp=None,
    )

    validate_request_meta(meta)


def test_validate_project_id_rejects_invalid_value() -> None:
    with pytest.raises(BridgeValidationError) as exc_info:
        validate_project_id("../bad-project")

    assert exc_info.value.code == INVALID_PROJECT_ID
    assert exc_info.value.target == "project_id"


def test_validate_scene_name_rejects_invalid_value() -> None:
    with pytest.raises(BridgeValidationError) as exc_info:
        validate_scene_name("bad scene name")

    assert exc_info.value.code == INVALID_SCENE_NAME
    assert exc_info.value.target == "scene_name"


def test_validate_entity_name_rejects_invalid_value() -> None:
    with pytest.raises(BridgeValidationError) as exc_info:
        validate_entity_name("bad/entity")

    assert exc_info.value.code == INVALID_ENTITY_NAME
    assert exc_info.value.target == "entity_name"


def test_validate_component_specs_accepts_camera_and_mesh() -> None:
    validate_component_specs(
        [
            ComponentSpec(type="Camera"),
            ComponentSpec(type="Mesh", asset_hint="Box_1x1.fbx"),
        ]
    )


def test_validate_request_model_accepts_valid_project_scan_request_without_approval() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-2002",
            tool_name="project_scan",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    validate_request_model("project_scan", request)


def test_validate_request_model_accepts_approval_required_tool_with_token() -> None:
    request = SceneOpenRequest(
        meta=RequestMeta(
            request_id="req-2003",
            tool_name="scene_open",
            dry_run=False,
            approval_token="approved-2003",
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
    )

    validate_request_model("scene_open", request)


def test_validate_request_model_rejects_approval_required_tool_without_token() -> None:
    request = SceneOpenRequest(
        meta=RequestMeta(
            request_id="req-2004",
            tool_name="scene_open",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        validate_request_model("scene_open", request)

    assert exc_info.value.code == APPROVAL_REQUIRED
    assert exc_info.value.target == "approval_token"


def test_validate_request_model_rejects_approval_required_tool_with_blank_token() -> None:
    request = SceneOpenRequest(
        meta=RequestMeta(
            request_id="req-2005",
            tool_name="scene_open",
            dry_run=False,
            approval_token="   ",
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        validate_request_model("scene_open", request)

    assert exc_info.value.code == APPROVAL_REQUIRED
    assert exc_info.value.target == "approval_token"


def test_validate_request_model_rejects_mismatched_meta_tool_name() -> None:
    request = SceneOpenRequest(
        meta=RequestMeta(
            request_id="req-2006",
            tool_name="scene_create",
            dry_run=False,
            approval_token="approved-2006",
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        validate_request_model("scene_open", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "meta.tool_name"


def test_validate_request_model_rejects_wrong_request_type() -> None:
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-2007",
            tool_name="project_scan",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        validate_request_model("scene_open", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "request_model"


def test_validate_request_model_accepts_entity_find_with_name_query() -> None:
    request = EntityFindRequest(
        meta=RequestMeta(
            request_id="req-2008",
            tool_name="entity_find",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        query=EntityFindQuery(entity_name="test_entity", match_mode="exact", limit=10),
    )

    validate_request_model("entity_find", request)


def test_validate_request_model_rejects_entity_find_without_search_criteria() -> None:
    request = EntityFindRequest(
        meta=RequestMeta(
            request_id="req-2009",
            tool_name="entity_find",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        query=EntityFindQuery(entity_name=None, entity_id=None, match_mode="exact", limit=10),
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        validate_request_model("entity_find", request)

    assert exc_info.value.code == INVALID_REQUEST
    assert exc_info.value.target == "query"


def test_validate_request_model_accepts_entity_find_with_entity_id_query() -> None:
    request = EntityFindRequest(
        meta=RequestMeta(
            request_id="req-2010",
            tool_name="entity_find",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        query=EntityFindQuery(entity_name=None, entity_id="entity-123", match_mode="contains", limit=5),
    )

    validate_request_model("entity_find", request)


def test_validate_request_model_accepts_entity_list_with_scene_scope() -> None:
    request = EntityListRequest(
        meta=RequestMeta(
            request_id="req-2011",
            tool_name="entity_list",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        scope="scene",
        limit=50,
    )

    validate_request_model("entity_list", request)


def test_validate_request_model_accepts_entity_list_with_root_scope() -> None:
    request = EntityListRequest(
        meta=RequestMeta(
            request_id="req-2012",
            tool_name="entity_list",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        scope="root_only",
        limit=50,
    )

    validate_request_model("entity_list", request)


def test_validate_request_model_accepts_entity_children_with_parent_lookup() -> None:
    request = EntityChildrenRequest(
        meta=RequestMeta(
            request_id="req-2013",
            tool_name="entity_children",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        parent_entity_id="entity-001",
        limit=25,
    )

    validate_request_model("entity_children", request)


def test_validate_request_model_accepts_entity_parent_with_child_lookup() -> None:
    request = EntityParentRequest(
        meta=RequestMeta(
            request_id="req-2014",
            tool_name="entity_parent",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        child_entity_id="entity-002",
    )

    validate_request_model("entity_parent", request)


def test_validate_request_model_accepts_entity_ancestors_with_child_lookup() -> None:
    request = EntityAncestorsRequest(
        meta=RequestMeta(
            request_id="req-2016",
            tool_name="entity_ancestors",
            dry_run=False,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        child_entity_id="entity-003",
        limit=8,
    )

    validate_request_model("entity_ancestors", request)


def test_validate_request_model_rejects_invalid_component_request() -> None:
    request = EntityCreateRequest(
        meta=RequestMeta(
            request_id="req-2017",
            tool_name="entity_create",
            dry_run=False,
            approval_token="approved-2017",
            timestamp=None,
        ),
        project_id="McpSandbox",
        scene_name="TestLevel01",
        entity_name="TestBoxEntity",
        components=[ComponentSpec.model_construct(type="Light", asset_hint=None)],
    )

    with pytest.raises(BridgeValidationError) as exc_info:
        validate_request_model("entity_create", request)

    assert exc_info.value.code == INVALID_COMPONENT
    assert exc_info.value.target == "components"
