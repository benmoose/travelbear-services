import attr

from .validation import get_required_field_error_message, get_type_mismatch_error_message

API_MODEL_FLAG = "__api_model__"


def api_model(cls):
    """
    API Model decorator for representing HTTP data from external sources.
    It is primarily responsible for
     - encoding data as fields in a class (for use in application code)
     - providing methods to check the validity of data.

    To activate validity checking, classes using this decorator should add the
    `get_validation_errors` method.
    """
    cls._from_dict = classmethod(api_model_from_dict)
    if not hasattr(cls, "from_dict"):
        cls.from_dict = classmethod(api_model_from_dict)

    cls._from_db_model = classmethod(api_model_from_db_model)
    if not hasattr(cls, "from_db_model"):
        cls.from_db_model = classmethod(api_model_from_db_model)

    cls._to_dict = api_model_to_dict
    if not hasattr(cls, "to_dict"):
        cls.to_dict = api_model_to_dict

    if not hasattr(cls, "get_validation_errors"):
        cls.get_validation_errors = lambda _: []

    cls._is_valid = property(api_model_is_valid)
    if not hasattr(cls, "is_valid"):
        cls.is_valid = property(api_model_is_valid)

    cls.__attrs_post_init__ = api_model_post_init

    setattr(cls, API_MODEL_FLAG, True)

    return attr.s(
        cls,
        these=api_model_get_ib_fields(cls.__slots__),
        slots=True,
        weakref_slot=False,
    )


def api_model_post_init(self):
    self.validation_errors = self.get_validation_errors()
    if hasattr(self, "__post_init__"):
        self.__post_init__()


def api_model_get_ib_fields(fields):
    mapping = {field: attr.ib(default=None) for field in fields}
    mapping["validation_errors"] = attr.ib(factory=list, repr=False)
    return mapping


def api_model_to_dict(self):
    dct = {}
    for attribute in attr.fields(self.__class__):
        if not attribute.repr:
            continue
        value = getattr(self, attribute.name, None)
        if value is None:
            continue
        if hasattr(value, API_MODEL_FLAG):
            dct[attribute.name] = value.to_dict()
        else:
            dct[attribute.name] = value
    return dct


def api_model_from_dict(cls, data):
    args = {}
    for attribute in cls.__slots__:
        value = data.get(attribute)
        if value is not None:
            args[attribute] = value
    return cls(**args)


def api_model_from_db_model(cls, db_model):
    args = {}
    for attribute in cls.__slots__:
        value = getattr(db_model, attribute, None)
        if value is not None:
            args[attribute] = value
    return cls(**args)


def api_model_is_valid(self):
    return not bool(self.validation_errors)
