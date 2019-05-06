import attr


@attr.s(auto_attribs=True)
class TwilioWebhookRequest:
    message_sid: str
    sms_sid: str
    messaging_service_sid: str = ""
    message_status: str = ""
    error_code: str = ""

    @classmethod
    def from_dict(cls, data):
        return cls(
            message_sid=data["message_sid"],
            sms_sid=data["sms_sid"],
            messaging_service_sid=data.get("messaging_service_sid"),
            message_status=data.get("message_status"),
            error_code=data.get("error_code"),
        )
