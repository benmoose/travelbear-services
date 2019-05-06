from common.model import data_model


@data_model
class TwilioSMSWebhookRequest:
    account_sid: str
    message_sid: str
    message_status: str
    sms_sid: str
    sms_status: str
    client_identity: str = ""
    instance_sid: str = ""
    messaging_service_sid: str = ""
    error_code: str = ""

    @classmethod
    def from_dict(cls, data):
        return cls(
            account_sid=data["AccountSid"],
            message_sid=data["MessageSid"],
            message_status=data["MessageStatus"],
            sms_sid=data["SmsSid"],
            sms_status=data["SmsStatus"],
            client_identity=data.get("ClientIdentity"),
            instance_sid=data.get("InstanceSid"),
            messaging_service_sid=data.get("MessagingServiceSid"),
            error_code=data.get("ErrorCode"),
        )
