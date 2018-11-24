AUTHORIZATION_HEADER_NAME = "Authorization"


def get_authorization_header(request):
    headers = request.META
    authorization_meta_name = get_meta_key_name(AUTHORIZATION_HEADER_NAME)
    return headers.get(authorization_meta_name)


def get_meta_key_name(header_name):
    """
    >>> get_meta_key_name('foo')
    'HTTP_FOO'
    """
    return f"HTTP_{header_name.upper()}"
