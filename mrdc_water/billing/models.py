from django.db import models

class WaterRate(models.Model):
    rate_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField(auto_now_add=True)  # Date when this rate became effective

    def __str__(self):
        return f"Rate: {self.rate_per_unit} (Effective from {self.effective_date})"

class MeterReading(models.Model):
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, related_name='meter_readings')
    reading_date = models.DateField()
    reading_value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reading on {self.reading_date} for {self.user.username}: {self.reading_value}"

class Bill(models.Model):
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, related_name='bills')
    meter_reading = models.ForeignKey(MeterReading, on_delete=models.CASCADE)
    previous_reading_value = models.DecimalField(max_digits=10, decimal_places=2)
    consumption = models.DecimalField(max_digits=10, decimal_places=2)
    rate_used = models.ForeignKey(WaterRate, on_delete=models.PROTECT)  # Link to the rate used for this bill
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    billing_period_start = models.DateField()
    billing_period_end = models.DateField()
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill for {self.user.username} ({self.billing_period_end})"