import uuid

from django.core.exceptions import ValidationError

from users.selectors.user import UserSelector


def validate_uuid4(value):
    """
    Validate that the provided value is a valid UUID4.
    """
    try:
        val = uuid.UUID(str(value), version=4)
    except ValueError:
        raise ValidationError("Invalid UUID format. Must be a valid UUID4.")
    if str(val) != str(value):
        raise ValidationError("Invalid UUID4 value.")
    return value


def validate_user_exists(value):
    """
    Validate that the user exists in the database.
    """
    user = UserSelector.get_user_by_id(value)
    if not user:
        raise ValidationError("User with this ID does not exist.")
    return value
