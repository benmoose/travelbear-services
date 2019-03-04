from django.db import transaction

from ..models import Move


def create_move(
    start_location, end_location, travel_method="", depart_time=None, arrive_time=None
):
    return Move.objects.create(
        start_location=start_location,
        end_location=end_location,
        travel_method=travel_method,
        depart_time=depart_time,
        arrive_time=arrive_time,
    )


def delete_move(move):
    with transaction.atomic():
        move = Move.objects.select_for_update().get(pk=move.pk)
        if move.is_deleted:
            return move
        move.is_deleted = True
        move.save(update_fields=["is_deleted", "modified_on"])
    return move


def get_move_by_move_id(user, move_id):
    try:
        return Move.objects.filter(start_location__trip__created_by=user).get(
            move_id=move_id, is_deleted=False
        )
    except Move.DoesNotExist:
        return None
