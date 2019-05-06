import attr


def data_model(cls):
    """
    Simple wrapper around `attrs`.

    All data model attributes require PEP 526 type annotations.

    Annotations are checked after instantiation and a TypeError is raised if there is
    a type mismatch.
    """
    cls.__attrs_post_init__ = data_model_post_init

    cls._from_dict = classmethod(data_model_from_dict)
    if not hasattr(cls, "from_dict"):
        cls.from_dict = classmethod(data_model_from_dict)

    return attr.s(cls, auto_attribs=True, slots=True)


def data_model_post_init(self):
    validate(self, attr.fields(self.__class__))


def validate(self, attributes):
    for attribute in attributes:
        value = getattr(self, attribute.name)
        validate_attribute(attribute, value)


def validate_attribute(attribute, value):
    if not isinstance(value, attribute.type):
        raise TypeError(
            f"expected type {attribute.type} for attribute '{attribute.name}', "
            f"but received type {type(value)}"
        )


def data_model_from_dict(cls, data: dict):
    attribute_name = {attrib.name for attrib in attr.fields(cls)}
    init_data = {k: v for k, v in data.items() if k in attribute_name and v is not None}
    return cls(**init_data)
