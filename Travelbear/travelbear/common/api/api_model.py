import attr

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

    cls._serialise = api_model_serialise
    if not hasattr(cls, "serialise"):
        cls.serialise = api_model_serialise

    if not hasattr(cls, "get_validation_errors"):
        cls.get_validation_errors = lambda _: []

    cls._is_valid = property(api_model_is_valid)
    if not hasattr(cls, "is_valid"):
        cls.is_valid = property(api_model_is_valid)

    cls.__attrs_post_init__ = api_model_post_init

    setattr(cls, API_MODEL_FLAG, True)

    return attr.s(
        these=api_model_get_attributes(cls.__slots__), slots=True, weakref_slot=False
    )(cls)


def api_model_post_init(self):
    self.validation_errors = self.get_validation_errors()
    if hasattr(self, "__post_init__"):
        self.__post_init__()


def api_model_get_attributes(slots):
    mapping = {slot: attr.ib(default=None) for slot in slots}
    mapping["validation_errors"] = attr.ib(factory=list, repr=False)
    return mapping


def api_model_serialise(self) -> dict:
    dct = {}
    for attribute in attr.fields(self.__class__):
        if not attribute.repr:
            continue
        value = getattr(self, attribute.name, None)
        if value is None or value == "":
            continue
        if hasattr(value, API_MODEL_FLAG):
            dct[attribute.name] = value.serialise()
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


def api_model_is_valid(self) -> bool:
    return not bool(self.validation_errors)


def is_api_model(cls) -> bool:
    return hasattr(cls, API_MODEL_FLAG)
