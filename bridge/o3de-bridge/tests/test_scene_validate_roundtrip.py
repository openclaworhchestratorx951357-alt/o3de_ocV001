from o3de_bridge.run_scene_validate_roundtrip import (
    DEFAULT_ENTITY_NAME,
    DEFAULT_PROJECT_ID,
    DEFAULT_SCENE_NAME,
    build_request,
)


def test_build_request_uses_scene_validate_contract() -> None:
    request = build_request(request_id="scene-validate-test-001")

    assert request.meta.request_id == "scene-validate-test-001"
    assert request.meta.tool_name == "scene_validate"
    assert request.project_id == DEFAULT_PROJECT_ID
    assert request.scene_name == DEFAULT_SCENE_NAME
    assert len(request.expected_entities) == 1
    assert request.expected_entities[0].entity_name == DEFAULT_ENTITY_NAME
    assert request.expected_entities[0].required_components == ["Camera", "Mesh"]
    assert request.meta.dry_run is True
