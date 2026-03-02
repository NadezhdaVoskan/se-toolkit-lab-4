"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_includes_interaction_with_different_learner_id() -> None:
    interactions = [_make_log(1, 2, 1)]
    result = _filter_by_item_id(interactions, 1)

    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].item_id == 1
    assert result[0].learner_id == 2


def test_filter_multiple_matching_items_returns_all() -> None:
    # When several logs share the same item_id, they should all be returned
    interactions = [
        _make_log(1, 1, 5),
        _make_log(2, 2, 5),
        _make_log(3, 3, 6),
        _make_log(4, 4, 5),
    ]
    result = _filter_by_item_id(interactions, 5)
    assert len(result) == 3
    assert {i.id for i in result} == {1, 2, 4}


def test_filter_returns_empty_when_no_match() -> None:
    interactions = [_make_log(1, 1, 10), _make_log(2, 2, 20)]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


def test_filter_handles_zero_and_negative_item_id() -> None:
    # item_id of zero or negative should be treated like any other integer
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, -1)]
    assert _filter_by_item_id(interactions, 0) == [interactions[0]]
    assert _filter_by_item_id(interactions, -1) == [interactions[1]]


def test_filter_does_not_modify_original_list() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    copy = list(interactions)
    _ = _filter_by_item_id(interactions, 1)
    assert interactions == copy

