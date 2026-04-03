from o3de_bridge.run_scene_open_roundtrip import (
    DEFAULT_APPROVAL_TOKEN,
    DEFAULT_PROJECT_ID,
    DEFAULT_SCENE_NAME,
    build_request,
)


def test_build_request_uses_scene_open_contract() -> None:
    request = build_request(request_id="scene-open-test-001")

    assert request.meta.request_id == "scene-open-test-001"
    assert request.meta.tool_name == "scene_open"
    assert request.meta.approval_token == DEFAULT_APPROVAL_TOKEN
    assert request.project_id == DEFAULT_PROJECT_ID
    assert request.scene_name == DEFAULT_SCENE_NAME
    assert request.meta.dry_run is False
