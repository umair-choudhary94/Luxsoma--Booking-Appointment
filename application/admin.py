from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import *
admin.site.register(StripeToken)
admin.site.register(CreditCard)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'price', 'category')
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'timestamp')

admin.site.site_header = 'Luxsomamedspa Administration'
admin.site.site_title = 'Luxsomamedspa'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'timestamp')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'appointment_date', 'price', 'start_time', 'end_time', 'payment_status', 'completion_status', 'created_at', 'deduct_amount_button')
    list_filter = ('payment_status', 'completion_status', 'appointment_date', 'start_time')
    search_fields = ('user__username', 'service__name')
    date_hierarchy = 'appointment_date'

    def deduct_amount_button(self, obj):
        payment_url = reverse('process_payment', args=[obj.id])
        return format_html(f'<a href="{payment_url}" type="button">Process Payment</a>')

    deduct_amount_button.short_description = "Deduct Amount"  # Custom column header for the button
    deduct_amount_button.allow_tags = True  # Allow HTML in the column