from django.contrib import admin
from .models import DlFromWebs

class DlFromWebsAdmin(admin.ModelAdmin):
	list_display = ('url_text', 'fecha', 'media_host')

	list_filter = ['media_host']

admin.site.register(DlFromWebs, DlFromWebsAdmin)