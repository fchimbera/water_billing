from django.contrib import admin
from .models import WaterRate, MeterReading, Bill
from .services import calculate_and_create_bill
from django.utils import timezone

@admin.register(WaterRate)
class WaterRateAdmin(admin.ModelAdmin):
    list_display = ('rate_per_unit', 'effective_date', 'is_active', 'description')
    list_filter = ('is_active',)
    search_fields = ('description',)

def generate_bill_action(modeladmin, request, queryset):
    count = 0
    errors = 0
    for reading in queryset.filter(is_billed=False):
        try:
            calculate_and_create_bill(reading)
            count += 1
        except Exception as e:
            modeladmin.message_user(request, f"Error billing reading {reading.id}: {e}", level='ERROR')
            errors += 1
    if count > 0:
        modeladmin.message_user(request, f"Successfully generated {count} bill(s).")
    if errors == 0 and count == 0:
        modeladmin.message_user(request, "Selected readings were already billed or no unbilled readings selected.", level='WARNING')

generate_bill_action.short_description = "Generate Bill for selected Readings"

@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ('user', 'reading_date', 'reading_value', 'is_billed', 'created_at')
    list_filter = ('reading_date', 'is_billed', 'user')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'reading_date'
    actions = [generate_bill_action]

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('user', 'billing_period_end', 'amount_due', 'consumption', 'due_date', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'billing_period_end', 'user')
    search_fields = ('user__username', 'user__email', 'meter_reading__id')
    date_hierarchy = 'billing_period_end'
    readonly_fields = ('user', 'meter_reading', 'previous_reading_value', 'consumption', 'rate_used', 'amount_due', 'billing_period_start', 'billing_period_end', 'created_at')
    # Add actions like 'Mark as Paid'
    def mark_as_paid(modeladmin, request, queryset):
        queryset.update(is_paid=True, paid_date=timezone.now().date())
    mark_as_paid.short_description = "Mark selected bills as Paid"

    actions = [mark_as_paid]