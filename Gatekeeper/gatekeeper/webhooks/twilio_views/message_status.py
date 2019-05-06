from django.views.decorators.http import require_POST

from common.response import success_response

from ..models.twilio_webhook_request import TwilioWebhookRequest


@require_POST
def message_status_webhook(request):
    return success_response()
