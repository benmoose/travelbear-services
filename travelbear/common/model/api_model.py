import attr
import typing


def api_model(cls):
    default_attribute_value = attr.ib(default=None)
    return attr.s(
        cls, these={slot: default_attribute_value for slot in cls.__slots__}, slots=True
    )


@attr.s(auto_attribs=True)
class APIModel:
    """
    Base class for serialising request data into a more useful form.

    Subclasses must define `get_validation_errors`, which should return
    a list of validation errors, or an empty list if there are none.
    """

    validation_errors: typing.List[str] = attr.ib(factory=list, init=False, repr=False)

    def __attrs_post_init__(self):
        self.validation_errors = self._get_validation_errors()

    def _get_validation_errors(self):
        validation_errors = self.get_validation_errors()
        if not isinstance(validation_errors, list):
            raise RuntimeError(
                f"get_validation_errors must return a list, got {type(validation_errors)}"
            )
        return validation_errors

    def to_dict(self):
        return attr.asdict(self)

    @property
    def is_valid(self):
        return not bool(self.validation_errors)

    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError

    def get_validation_errors(self):
        raise NotImplementedError
