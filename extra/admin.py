from django.contrib import admin

from extra.models import TextBit, Title

class ProperDisplay(admin.ModelAdmin):
    list_display = ('__unicode__',)

admin.site.register(TextBit, ProperDisplay)
admin.site.register(Title, ProperDisplay)
