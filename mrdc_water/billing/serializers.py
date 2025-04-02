from rest_framework import serializers
from .models import MeterReading, Bill, WaterRate

class WaterRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterRate
        fields = '__all__'

class MeterReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeterReading
        fields = ['reading_date', 'reading_value']

class BillSerializer(serializers.ModelSerializer):
    water_rate = WaterRateSerializer(read_only=True)
    meter_reading = MeterReadingSerializer(read_only=True)

    class Meta:
        model = Bill
        fields = '__all__'
        read_only_fields = ['user', 'previous_reading_value', 'consumption', 'rate_used', 'amount_due', 'billing_period_start', 'billing_period_end']