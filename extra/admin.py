from django.contrib import admin

from extra.models import TextBit

class ProperDisplay(admin.ModelAdmin):
    list_display = ('__unicode__',)

admin.site.register(TextBit, ProperDisplay)
