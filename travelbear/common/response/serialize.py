from django.core.serializers.json import DjangoJSONEncoder

from common.api import is_api_model


class APIModelJSONSerializer(DjangoJSONEncoder):
    def default(self, o):
        if is_api_model(o.__class__):
            return o.serialise()
        return super().default(o)
