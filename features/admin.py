from features.models import Post, Feature
from django.contrib import admin



#class PostAdmin(admin.ModelAdmin):
#    list_display = ["title", "publish", "status"]
#    list_filter = ["publish", "status"]
#    search_fields = ["title", "body", "tease"]
#    prepopulated_fields = {"slug": ["title"]}

class FeatureAdmin(admin.ModelAdmin):
    list_display = ["title", "publish", "status", "sharetype","geomtype", "feature_of"]
    list_filter = ["publish", "status","feature_of"]
    search_fields = ["title", "body", "tease"]
    prepopulated_fields = {"slug": ["title"]}
    
#admin.site.register(Project2, Project2Admin)
#admin.site.register(Project, ProjectAdmin)
admin.site.register(Feature, FeatureAdmin)