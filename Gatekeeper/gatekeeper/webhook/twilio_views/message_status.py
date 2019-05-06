from django.views.decorators.http import require_POST

from common.response import success_response

from ..models.twilio_webhook_request import TwilioSMSWebhookRequest


@require_POST
def message_status_webhook(request):
    request_data = get_request_data(request.POST)
    return success_response({"status": request_data.message_status})


def get_request_data(data: dict) -> TwilioSMSWebhookRequest:
    return TwilioSMSWebhookRequest.from_dict(data)
