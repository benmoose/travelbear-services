def count_models_in_db(model):
    return len(model.objects.all())
