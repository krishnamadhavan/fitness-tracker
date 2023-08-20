from datetime import date

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError


def validate_date_of_birth(value: date) -> None:
    """
        Validate that the provided date is a valid date of birth.

        This validator function checks if the provided date is in the past,
        ensuring that it can be considered a valid date of birth. It raises
        a ValidationError if the date is not in the past.

        Args:
            value (date): The date to be validated.

        Raises:
            ValidationError: If the provided date is in the future.

        Example usage:
        ```
        date_of_birth = models.DateField(validators=[validate_date_of_birth])
        ```

    """
    if value >= timezone.now().date():
        raise ValidationError(
            detail={
                "date_of_birth": _("Date of birth must be in the past."),
            }
        )
