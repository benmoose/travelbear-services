import json


def safe_parse_json(json_string):
    try:
        return json.loads(json_string)
    except AssertionError:
        raise
    except json.decoder.JSONDecodeError:
        return None
