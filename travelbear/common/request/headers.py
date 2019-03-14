from typing import Optional

AUTHORIZATION_HEADER_NAME = "Authorization"


def get_authorization_header(request_headers: dict) -> Optional[str]:
    """
    >>> get_authorization_header(dict(HTTP_AUTHORIZATION="the key", HTTP_FOO="foo"))
    'the key'
    >>> get_authorization_header(dict(HTTP_FOO="foo")) is None
    True
    """
    authorization_meta_name = get_meta_key_name(AUTHORIZATION_HEADER_NAME)
    return request_headers.get(authorization_meta_name)


def get_meta_key_name(header_name: str) -> str:
    """
    >>> get_meta_key_name('foo')
    'HTTP_FOO'
    """
    return f"HTTP_{header_name.upper()}"
