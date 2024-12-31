import re


def check_strong_password(password):
    """Check if a password is strong.

    Args:
        password (str): The password to check.

    Returns:
        bool: True if the password is strong, otherwise False.
    """
    if len(password) < 8:
        return False

    if not re.search(r'[A-Z]', password):
        return False

    if not re.search(r'[a-z]', password):
        return False

    if not re.search(r'\d', password):
        return False

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True
