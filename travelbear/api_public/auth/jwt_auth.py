import functools
import os
from pathlib import Path

import jwt

from common.request import get_authorization_header


PUBLIC_KEY_NAME = 'travel-bear.pem'
PUBLIC_KEY_PATH = Path(__file__).parent / PUBLIC_KEY_NAME


def require_jwt_auth(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        auth_header = get_authorization_header(request)
        if auth_header is None:
            request.user = None

        token = get_token_from_authorization_header(auth_header)
        try:
            claims = decode_token(token)
        except Exception:
            request.user = None
        request.user = claims['sub']


def decode_token(token):
    public_key = get_jwt_public_key()
    return jwt.decode(token, public_key, algorithms=['RSA256'])


def get_jwt_public_key():
    """
    TODO(Ben): Make this less hacky
    >>> type(get_jwt_public_key()) == str
    True
    """
    with open(PUBLIC_KEY_PATH) as f:
        return f.read()


def get_token_from_authorization_header(authorization_header):
    """
    >>> get_token_from_authorization_header('Bearer: foo')
    'foo'
    >>> get_token_from_authorization_header('Bearer:') is None
    True
    >>> get_token_from_authorization_header('foo') is None
    True
    """
    try:
        bearer, token = authorization_header.split(':')
        token = token.strip()
        return token if len(token) > 0 else None
    except ValueError:
        return None
