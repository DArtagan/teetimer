from django.contrib import admin

from tracker.models import TeeTime

class ProperDisplay(admin.ModelAdmin):
    list_display = ('__unicode__',)

admin.site.register(TeeTime, ProperDisplay)
