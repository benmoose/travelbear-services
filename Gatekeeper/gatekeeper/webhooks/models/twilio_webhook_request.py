import attr


@attr.s(auto_attribs=True)
class TwilioWebhookRequest:
    message_sid: str
    sms_sid: str
    messaging_service_sid: str = ""
    message_status: str = ""
    error_code: str = ""
