from random import choices


def generate_verification_code(population: str, length: int) -> str:
    """
    >>> import re
    >>> re.match("^[123]{3}$", generate_verification_code("123", 3)) is not None
    True
    """
    if length < 0:
        raise ValueError("length cannot be less than 0")
    return "".join(choices(population, k=length))
