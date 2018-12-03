from db_layer.trip import Move


def create_move(start_location, end_location, travel_method="", depart_time=None, arrive_time=None):
    return Move.objects.create(
        start_location=start_location,
        end_location=end_location,
        travel_method=travel_method,
        depart_time=depart_time,
        arrive_time=arrive_time,
    )
