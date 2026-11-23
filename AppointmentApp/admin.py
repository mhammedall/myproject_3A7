from django.contrib import admin
from .models import Appointment
from AccountApp.models import Doctor

class DocteurPerso(admin.StackedInline):
    model=Doctor
@admin.register(Appointment)
class AppointmentAdminPers(admin.ModelAdmin):
    inlines = [DocteurPerso]
    list_display=( 'reason','status','duration_minutes','appointment_date')
    list_filter=('status','appointment_date')
    list_editable=('status',)
    list_per_page = 2
    ordering=('appointment_date',)
    fieldsets=(
        ('Description',{
            'fields': ('reason', 'status')
        }),
        ('date+duration' , {
            'fields': ('appointment_date', 'duration_minutes')
        }),
    )
    ('patients/doctors' , {
                'fields': ('doctor', 'patient')
            }),
('plannification' , {
            'fields': ('created_at', 'updated_at')
        }),
readonly_fields=('created_at', 'updated_at')