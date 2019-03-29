"""
Module contain django admin models
"""

from django.contrib import admin

from .tasks import send_report
from .models import Client


def send_report_action(modeladmin, request, queryset):
    clients_id = list(map(lambda client: client.id, queryset))
    send_report.delay(clients_id)


send_report_action.short_description = "Send report"


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'likes')
    actions = [send_report_action]


admin.site.register(Client, ClientAdmin)
