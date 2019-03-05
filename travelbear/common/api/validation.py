from typing import List, Type


def required_fields(self, fields):
    errors = []
    for field in fields:
        if getattr(self, field) is None:
            errors.append(get_required_field_error_message(field))
    return errors


def get_required_field_error_message(field_name: str) -> str:
    """
    >>> get_required_field_error_message("foo")
    "'foo' is a required field"
    """
    return f"'{field_name}' is a required field"


def get_type_mismatch_error_message(field_name: str, expected_types: List[Type]) -> str:
    """
    >>> get_type_mismatch_error_message("foo", [type(True)])
    "'foo' must be of type bool"
    >>> get_type_mismatch_error_message(5, [type(True), str])
    "'5' must be one of types bool, str"
    """
    if len(expected_types) == 1:
        return f"'{field_name}' must be of type {expected_types[0].__name__}"
    type_names = [expected_type.__name__ for expected_type in expected_types]
    return f"'{field_name}' must be one of types {', '.join(type_names)}"
