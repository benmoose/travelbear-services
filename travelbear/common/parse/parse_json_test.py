import pytest

from .parse_json import safe_parse_json


@pytest.mark.parametrize(
    "input_string, expected",
    (
        ('{"foo": "bar"}', dict(foo="bar")),
        ('"foo": "bar"', None),
        ("", None),
        ("fnajeb jefn-wj", None),
        ("[1, 2, 3, 4]", [1, 2, 3, 4]),
        ('[1, 2, {"a": 3}, 4]', [1, 2, dict(a=3), 4]),
        ('{"a": null}', dict(a=None)),
    ),
)
def test_safe_parse_json_on_valid_input(input_string, expected):
    assert safe_parse_json(input_string) == expected
