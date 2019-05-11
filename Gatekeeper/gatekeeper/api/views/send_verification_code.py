import re
from typing import Optional

from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from phonenumbers import PhoneNumberFormat, format_number, parse

from common.model import data_model
from common.response import error_response, success_response
from coms.providers import get_communication_provider
from webhook.twilio_views.message_status import message_status_webhook

STRING_LIKELY_MOBILE_NUMBER = re.compile(r"07\d{9}")


@data_model
class RequestData:
    phone_number: str


@require_POST
def send_verification_code(request) -> HttpResponse:
    request_data = get_request_data(request.POST)
    if request_data is None:
        return error_response()

    phone_number = get_e164_phone_number(request_data.phone_number, "GB")
    if phone_number is None:
        return error_response("invalid phone_number")

    provider = get_communication_provider()
    provider.send_sms(phone_number, "", reverse(message_status_webhook))

    return success_response({"phone_number": request_data.phone_number})


def get_request_data(request_body: dict) -> Optional[RequestData]:
    try:
        return RequestData.from_dict(request_body)
    except TypeError:
        return None


def get_e164_phone_number(phone_number: str, region: str) -> Optional[str]:
    """
    >>> get_e164_phone_number("+447000000000", "GB")
    '+447000000000'
    >>> get_e164_phone_number("07-000 000 00 0", "GB")
    '+447000000000'
    >>> get_e164_phone_number("07000000000", "GB")
    '+447000000000'
    >>> get_e164_phone_number("07000000000", "US")
    '+107000000000'
    >>> get_e164_phone_number("7000000000", "GB")
    '+447000000000'
    >>> get_e164_phone_number("+447a0000000b", "GB")
    '+4470000000'
    >>> get_e164_phone_number("", "GB")
    >>> get_e164_phone_number("abcdefg", "GB")
    """
    try:
        parsed_phone_number = parse(phone_number, region=region)
        return format_number(parsed_phone_number, PhoneNumberFormat.E164)
    except Exception:
        return None


def generate_verification_code():
    pass
