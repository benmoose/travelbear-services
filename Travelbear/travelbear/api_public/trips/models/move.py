from common.api import api_model

from .location import Location


@api_model
class Move:
    __slots__ = (
        "move_id",
        "arrive_time",
        "depart_time",
        "start_location_id",
        "end_location_id",
        "travel_method",
    )

    @classmethod
    def from_db_model(cls, db_model, start_location, end_location):
        return cls(
            move_id=db_model.move_id,
            arrive_time=db_model.arrive_time,
            depart_time=db_model.depart_time,
            start_location_id=start_location.location_id,
            end_location_id=end_location.location_id,
            travel_method=db_model.travel_method,
        )


class MoveArrival(Move):
    pass


class MoveDeparture(Move):
    pass
