from django.core.serializers.json import DjangoJSONEncoder


class APIModelJSONSerializer(DjangoJSONEncoder):
    def default(self, o):
        if hasattr(o, "__api_model__"):
            return o.to_dict()
        return super().default(o)
