from o3de_bridge.run_entity_create_roundtrip import (
    DEFAULT_ENTITY_NAME,
    DEFAULT_PROJECT_ID,
    DEFAULT_SCENE_NAME,
    build_request,
)


def test_build_request_uses_entity_create_contract() -> None:
    request = build_request(request_id="entity-create-test-001")

    assert request.meta.request_id == "entity-create-test-001"
    assert request.meta.tool_name == "entity_create"
    assert request.project_id == DEFAULT_PROJECT_ID
    assert request.scene_name == DEFAULT_SCENE_NAME
    assert request.entity_name == DEFAULT_ENTITY_NAME
    assert [component.type for component in request.components] == ["Camera", "Mesh"]
    assert request.meta.dry_run is False
