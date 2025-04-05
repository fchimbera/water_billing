from datetime import date, timedelta
from django.utils import timezone
from .models import MeterReading, Bill, WaterRate
from django.db.models import Max
from decimal import Decimal

"""
#Calculates water consumption and creates a bill based on a new meter reading.
# It checks for the latest previous reading, calculates the consumption, and creates a bill entry.
# It also handles the case where there is no previous reading by using the user's account creation date as the start of the billing period.
def calculate_and_create_bill(current_reading: MeterReading):
    
    user = current_reading.user
    previous_reading = MeterReading.objects.filter(user=user).exclude(id=current_reading.id).order_by('-reading_date').first()

    if previous_reading:
        previous_reading_value = previous_reading.reading_value
        consumption = current_reading.reading_value - previous_reading_value
        billing_period_start = previous_reading.reading_date
    else:
        previous_reading_value = 0
        consumption = current_reading.reading_value
        # If no previous reading, start of billing period could be account creation or a predefined date
        billing_period_start = user.date_joined.date() # Or you can set a default start date

    # Determine the billing period end (usually the date of the current reading)
    billing_period_end = current_reading.reading_date

    # Get the current water rate
    try:
        water_rate = WaterRate.objects.latest('effective_date')
    except WaterRate.DoesNotExist:
        raise ValueError("No water rate defined.")

    # Calculate the amount due
    amount_due = consumption * water_rate.rate_per_unit

    # Calculate the due date (e.g., 15 days after the billing period end)
    due_date = billing_period_end + timedelta(days=15)

    # Create the bill
    Bill.objects.create(
        user=user,
        meter_reading=current_reading,
        previous_reading_value=previous_reading_value,
        consumption=consumption,
        rate_used=water_rate,
        amount_due=amount_due,
        billing_period_start=billing_period_start,
        billing_period_end=billing_period_end,
        due_date=due_date
    )
"""

def calculate_and_create_bill(meter_reading):
    if meter_reading.is_billed:
        raise ValueError(f"Meter reading {meter_reading.id} is already billed.")

    user = meter_reading.user

    # Find the latest previous reading for the user
    previous_reading = MeterReading.objects.filter(
        user=user,
        reading_date__lt=meter_reading.reading_date,
        is_billed=True
    ).order_by('-reading_date').first()

    previous_reading_value = previous_reading.reading_value if previous_reading else Decimal('0.00')
    consumption = meter_reading.reading_value - previous_reading_value

    # Get the active water rate
    active_rate = WaterRate.objects.filter(effective_date__lte=meter_reading.reading_date, is_active=True).order_by('-effective_date').first()
    if not active_rate:
        raise ValueError("No active water rate found for this reading date.")

    amount_due = consumption * active_rate.rate_per_unit

    # Determine billing period (basic example)
    billing_period_start = previous_reading.reading_date if previous_reading else meter_reading.reading_date - timezone.timedelta(days=30) # Approximate
    billing_period_end = meter_reading.reading_date
    due_date = billing_period_end + timezone.timedelta(days=15)

    bill = Bill.objects.create(
        user=user,
        meter_reading=meter_reading,
        previous_reading_value=previous_reading_value,
        consumption=consumption,
        rate_used=active_rate,
        amount_due=amount_due,
        billing_period_start=billing_period_start,
        billing_period_end=billing_period_end,
        due_date=due_date
    )

    meter_reading.is_billed = True
    meter_reading.save()

    return bill