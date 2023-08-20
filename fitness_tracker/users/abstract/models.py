from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderChoices:
    """
        A class defining choices for gender in a Django model.

        Provides a set of predefined choices for representing gender options
        in a model. These choices can be used in a CharField with choices to
        ensure consistent and meaningful representation of gender data.

        Example usage:
        ```
        class YourModel(models.Model):
            gender = models.CharField(
                max_length=1,
                choices=YourModelChoices.GENDER_CHOICES,
                default=YourModelChoices.MALE,
            )
        ```

        Attributes:
            MALE: A string representing the 'Male' gender option.
            FEMALE: A string representing the 'Female' gender option.
            OTHER: A string representing the 'Other' gender option.
            PREFER_NOT_TO_SAY: A string representing the 'Prefer Not to Say' option.
            CHOICES: A tuple of tuples containing all available gender choices.

    """
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    PREFER_NOT_TO_SAY = "N"

    CHOICES = (
        (MALE, _("Male")),
        (FEMALE, _("Female")),
        (OTHER, _("Other")),
        (PREFER_NOT_TO_SAY, _("Prefer Not to Say"))
    )


class MobileNumberField(models.CharField):
    """
        A custom Django model field for storing mobile numbers.

        This custom field extends the CharField to validate and store
        mobile numbers. It enforces the requirement that the mobile number
        must be a valid 10-digit number. This field is designed to be used
        for storing Indian mobile numbers in your models.

        Example usage:
        ```
        class YourModel(models.Model):
            mobile_number = MobileNumberField()
        ```

        Attributes:
            default_validators: A list of default validators including
                a regex validator for 10-digit numbers.

    """
    default_validators = [
        RegexValidator(
            regex=r'^\d{10}$',
            message='Enter a valid 10-digit mobile number.',
            code='invalid_mobile_number'
        ),
    ]

    def __init__(self, *args, **kwargs):
        """
            Initialize the MobileNumberField.

            This method sets the max_length to 10 characters to match the
            10-digit format of Indian mobile numbers.

        """
        kwargs['max_length'] = 10
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        """
            Deconstruct the MobileNumberField.

            This method removes the max_length attribute from the field's
            deconstruction for better compatibility with migrations.

        """
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs
