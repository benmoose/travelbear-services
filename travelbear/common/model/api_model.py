import attr


def api_model(cls):
    """
    API Model decorator for representing input from external sources.
    It is primarily responsible for
     - encoding incoming data in a class (for easy use in application code)
     - providing methods to check the validity of data.

    To activate validity checking, classes using this decorator should add the `get_validation_errors`
    method.
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

    cls.__api_model__ = True

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


def api_model_to_dict(self, keep_empty_fields=False):
    return attr.asdict(
        self, filter=lambda k, v: _filter_attributes(k, v, keep_empty_fields)
    )


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


def _filter_attributes(attribute, value, keep_empty_keys):
    pass_key = attribute.repr
    pass_value = keep_empty_keys or value is not None
    return pass_key and pass_value
