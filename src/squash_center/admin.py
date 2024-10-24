from django.contrib import admin

from .models import RentalEquipment, RentalRecord, SquashCourt


# Inline for editing rental records right on the equipment page
class RentalRecordInline(admin.TabularInline):
    model = RentalRecord
    extra = 1  # number of empty rows to add


@admin.register(SquashCourt)
class SquashCourtAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_operational')
    list_filter = ('is_operational',)  # filter by court availability
    search_fields = ('name',)  # court name search


@admin.register(RentalEquipment)
class RentalEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price_per_hour')
    inlines = [RentalRecordInline]  # connect an inline to edit lease records
    search_fields = ('name', 'description')  # search by equipment name and description


@admin.register(RentalRecord)
class RentalRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'equipment', 'court', 'start_time', 'end_time')
    list_filter = ('court', 'start_time', 'end_time')  # court and time filter
    search_fields = ('user__email', 'court__name')  # search by user email and court name
