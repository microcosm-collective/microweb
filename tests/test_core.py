from core.api.resources import join_path_fragments
from pytest import raises


def test_api_resources_join_path_fragments():
    joined = join_path_fragments(["path", "to", "nowhere"])
    assert joined == "/path/to/nowhere"

    joined = join_path_fragments(["double", "/", "slash"])
    assert joined == "/double//slash"

    with raises(Exception):
        joined = join_path_fragments(["bad", "mix/ed", "slash"])
