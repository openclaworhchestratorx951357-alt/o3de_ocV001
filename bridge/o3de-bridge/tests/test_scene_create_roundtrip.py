from o3de_bridge.run_scene_create_roundtrip import (
    DEFAULT_PROJECT_ID,
    DEFAULT_SCENE_NAME,
    DEFAULT_TEMPLATE,
    build_request,
)


def test_build_request_uses_scene_create_contract() -> None:
    request = build_request(request_id="scene-create-test-001")

    assert request.meta.request_id == "scene-create-test-001"
    assert request.meta.tool_name == "scene_create"
    assert request.project_id == DEFAULT_PROJECT_ID
    assert request.scene_name == DEFAULT_SCENE_NAME
    assert request.template == DEFAULT_TEMPLATE
    assert request.meta.dry_run is False
