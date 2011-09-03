from django.contrib import admin
from seasons.models import Season

from actions import export_as_csv
admin.site.add_action(export_as_csv)

class SeasonAdmin(admin.ModelAdmin):
    list_display = ["name", "start", "end", "color"]
    search_fields = ["name"]
    list_editable = ["color"]
        

admin.site.register(Season, SeasonAdmin)