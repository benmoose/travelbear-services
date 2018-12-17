class UpdateNotAllowed(AttributeError):
    pass


def get_fields_to_update(updatable_fields, received_fields):
    # <= means `issubset`, dict_keys objects don't provide this as a named method
    if not received_fields <= updatable_fields:
        formatted_fields = ", ".join(received_fields - updatable_fields)
        raise UpdateNotAllowed(f"Cannot update fields: {formatted_fields}")
    return received_fields
