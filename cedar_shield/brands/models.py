from django.core.exceptions import ValidationError
from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)
    contract_number = models.CharField(max_length=100)
    contact_email = models.EmailField()
    payment_info = models.TextField()

    # Royalty payout fields
    payout_seller = models.FloatField(help_text="Percentage to seller (0-100)")
    payout_brand = models.FloatField(help_text="Percentage to brand (0-100)")
    payout_previous_owner = models.FloatField(help_text="Percentage to previous owner (0-100)")
    payout_platform = models.FloatField(help_text="Percentage to Phigitals platform (0-100)")

    # Reporting settings
    reporting_email = models.EmailField()
    reporting_frequency = models.CharField(
        max_length=50,
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        default='monthly'
    )
    platform_reporting_frequency = models.CharField(
        max_length=50,
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        default='monthly'
    )

    def clean(self):
        total = (
            self.payout_seller +
            self.payout_brand +
            self.payout_previous_owner +
            self.payout_platform
        )
        if round(total, 2) != 100.0:
            raise ValidationError(f"Payout percentages must add up to 100%. Current total: {total:.2f}%")

    def __str__(self):
        return self.name
