from common.model import api_model, validation


@api_model
class Move:
    __slots__ = ("start_location", "end_location")

    def get_validation_errors(self):
        errors = validation.required_fields(self, ["start_location", "end_location"])
        errors += validation.of_type(self, ["start_location", "end_location"], str)
        return errors
