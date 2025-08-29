# your_app/admin.py

from django.contrib import admin
from .models import QRCode

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('link', 'qr_code', 'created_at')
    readonly_fields = ('qr_code', 'created_at') # Make qr_code read-only in admin