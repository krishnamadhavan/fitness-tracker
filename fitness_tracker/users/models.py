from typing import Iterable

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from fitness_tracker.users.abstract.models import GenderChoices, MobileNumberField, FitnessGoalChoices
from fitness_tracker.users.validators import validate_date_of_birth


class User(AbstractUser):
    """
    Default custom user model for Fitness Tracker.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class FitnessProfile(models.Model):
    user = models.OneToOneField(
        to=User, verbose_name=_("User Profile"), on_delete=models.CASCADE, related_name="userprofile"
    )
    gender = models.CharField(
        _("Gender"),
        max_length=11,
        choices=GenderChoices.CHOICES,
        default=GenderChoices.MALE,
        help_text=_("Select the gender of the user.")
    )
    date_of_birth = models.DateField(
        _("Date of Birth"),
        validators=[validate_date_of_birth],
        help_text=_("Enter the date of birth of the user.")
    )
    age = models.PositiveIntegerField(
        _("Age in years"),
        null=True,
        blank=True,
        help_text=_("The calculated age of the user in years.")
    )
    contact_number = MobileNumberField(
        verbose_name=_("Mobile Number of the User"),
        help_text=_("Enter the mobile number of the user.")
    )
    height = models.PositiveIntegerField(
        _("Height (cm)"),
        help_text='Enter your height in centimeters.',
        validators=[
            MinValueValidator(1, message='Height must be a positive value.'),
        ]
    )
    weight = models.PositiveIntegerField(
        _("Weight (kg)"),
        help_text='Enter your weight in kilograms.',
        validators=[
            MinValueValidator(1, message='Weight must be a positive value.'),
        ]
    )
    bmi = models.FloatField(
        _("Body Mass Index"),
        help_text='Calculated Body Mass Index (BMI). Automatically populated.',
        blank=True,
        null=True
    )
    joining_date = models.DateField(
        _("Joining Date"),
        help_text=_("Enter the date when the user joined."),
        null=True,
        blank=True
    )
    goal = models.CharField(
        _("Fitness Goal"),
        max_length=2,
        choices=FitnessGoalChoices.CHOICES,
        default=FitnessGoalChoices.GENERAL_FITNESS,
        help_text=_("Select the fitness goal of the user.")
    )

    def calculate_age(self) -> int:
        """
            Calculate the age of the person based on date of birth.

            This method calculates the age of the person using the provided
            date of birth and the current date. The result is rounded down
            to the nearest whole year.

            Returns:
                int: The calculated age of the person in years.

            Example:
                If the date of birth is '1990-05-15', and the current date
                is '2023-08-30', the calculated age will be 33.

        """
        today = timezone.now().date()
        delta = today - self.date_of_birth
        return delta.days // 365

    def calculate_bmi(self) -> float:
        """
        Calculate the Body Mass Index (BMI) based on height and weight.

        BMI is calculated using the formula: weight (kg) / (height (m))^2.
        The result is rounded to two decimal places.

        Returns:
            float: The calculated BMI.

        """
        height_in_meters = self.height / 100
        bmi = self.weight / (height_in_meters ** 2)
        return round(bmi, 2)

    def save(
        self,
        force_insert: bool = ...,
        force_update: bool = ...,
        using: str | None = ...,
        update_fields: Iterable[str] | None = ...,
    ) -> None:
        self.age = self.calculate_age()
        self.bmi = self.calculate_bmi()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
