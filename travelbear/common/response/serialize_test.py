import json

from common.model import api_model

from .serialize import APIModelJSONSerializer


@api_model
class Foo:
    __slots__ = ("a", "b")


def test_api_model_json_serializer():
    foo = Foo(1, 2)
    assert json.dumps(foo, cls=APIModelJSONSerializer) == json.dumps({"a": 1, "b": 2})

    foo_nested = Foo(foo, [1, 2, 3])
    assert json.dumps(foo_nested, cls=APIModelJSONSerializer) == json.dumps(
        {"a": {"a": 1, "b": 2}, "b": [1, 2, 3]}
    )
