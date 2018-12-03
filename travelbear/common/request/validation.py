def required_fields(self, fields):
    errors = []
    for field in fields:
        if getattr(self, field) is None:
            errors.append(f"{field} is a required field")
    return errors


def of_type(self, fields, required_type):
    errors = []
    for field in fields:
        value = getattr(self, field)
        if not isinstance(value, required_type):
            errors.append(f"{field} must be of type {required_type}")
    return errors
