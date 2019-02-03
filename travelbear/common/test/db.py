def count_models_in_db(model):
    return len(model.objects.all())


def no_models_in_db(model):
    return 0 == count_models_in_db(model)
