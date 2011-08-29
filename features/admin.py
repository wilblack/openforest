from features.models import Post, Feature, Product, ProductType, FeatureType
from django.contrib import admin



#class PostAdmin(admin.ModelAdmin):
#    list_display = ["title", "publish", "status"]
#    list_filter = ["publish", "status"]
#    search_fields = ["title", "body", "tease"]
#    prepopulated_fields = {"slug": ["title"]}

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "type"]
    search_fields = ["name", "type"]
        
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "about"]
    search_fields = ["name", "about"]       

class FeatureAdmin(admin.ModelAdmin):
    list_display = ["title", "publish", "status", "geomtype", "feature_of","featuretype",'image']
    list_filter = ["publish", "status","feature_of"]
    list_editable = ['status',]
    search_fields = ["title", "body", "tease"]
    prepopulated_fields = {"slug": ["title"]}

class FeatureTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "about", 'geomtype']
    list_filter = ["geomtype"]
    search_fields = ["name", "about"]
     
    
#admin.site.register(Project2, Project2Admin)
#admin.site.register(Project, ProjectAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(FeatureType, FeatureTypeAdmin)