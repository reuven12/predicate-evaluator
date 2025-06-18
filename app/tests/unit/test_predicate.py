import pytest
from types import SimpleNamespace
from predicate.predicate import Predicate


def test_predicate_from_json_and_true():
    json_str = '{"feature": ".x.y", "operation": {"operator": "isNotNone"}}'
    pred = Predicate.from_json(json_str)
    obj = SimpleNamespace(x=SimpleNamespace(y=123))
    assert pred.evaluate(obj)


def test_predicate_from_json_and_false():
    json_str = '{"feature": ".x.y", "operation": {"operator": "isNone"}}'
    pred = Predicate.from_json(json_str)
    obj = SimpleNamespace(x=SimpleNamespace(y=123))
    assert not pred.evaluate(obj)


def test_predicate_invalid_path():
    json_str = '{"feature": ".x._bad", "operation": {"operator": "isNotNone"}}'
    pred = Predicate.from_json(json_str)
    obj = SimpleNamespace(x=SimpleNamespace(_bad=123))

    with pytest.raises(ValueError):
        pred.evaluate(obj)


def test_predicate_empty_path():
    json_str = '{"feature": "", "operation": {"operator": "isNotNone"}}'
    pred = Predicate.from_json(json_str)
    obj = SimpleNamespace()
    assert pred.evaluate(obj)


def test_predicate_to_dict():
    json_str = '{"feature": ".x.y", "operation": {"operator": "isNone"}}'
    pred = Predicate.from_json(json_str)
    expected = {
        "feature": ".x.y",
        "operation": {
            "operator": "isNone"
        }
    }
    assert pred.to_dict() == expected
