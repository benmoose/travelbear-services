def count_models_in_db(model) -> int:
    return len(model.objects.all())


def no_models_in_db(model) -> bool:
    return 0 == count_models_in_db(model)
