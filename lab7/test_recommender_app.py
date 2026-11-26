import tensorflow_recommenders as tfrs
from lab7 import recommender_app as app
from lab7.recommender_app import recommend


def test_uses_fork_source():
    assert "site-packages" not in tfrs.__file__


def test_baseline_topk():
    ids, _ = recommend("u1", k=3)
    assert ids == ["a", "b", "c"]


def test_invariant_ordering_and_size():
    ids, scores = recommend("u1", k=3)
    assert len(ids) == 3
    assert scores == sorted(scores, reverse=True)


def test_user_without_history_unchanged():
    app.USER_EMB["u2"] = app.USER_EMB["u1"]
    ids, _ = recommend("u2", k=3)
    assert ids == ["a", "b", "c"]