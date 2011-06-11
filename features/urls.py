from django.conf.urls.defaults import *

from features import views, models
from features.forms import *

urlpatterns = patterns("",
    # blog post
    url(r"^post/(?P<username>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$", "features.views.post", name="blog_post"),
    
    # blog post
    #url(r"^feature/(?P<username>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$", "features.views.feature", name="feature"),
    
    # all blog posts
    url(r"^$", "features.views.features", name="feature_list_all"),
    
    # blog post for user
    url(r"^posts/(?P<username>\w+)/$", "features.views.features", name="feature_list_user"),
    
    # your posts
    url(r"^your_posts/$", "features.views.your_posts", name="feature_list_yours"),
    
    # new blog post
    url(r"^new/$", "features.views.new", name="features_new"),
    
    # edit blog post
    url(r"^edit/(\d+)/$", "features.views.edit", name="feature_edit"),
    
    #destory blog post
    url(r"^destroy/(\d+)/$", "features.views.destroy", name="feature_destroy"),
    
    # API STUFF
    url(r"^list.json","features.views.list", name="feature_list_json"),
    url(r"^update.json","features.views.update", name="feature_update_json"),
    
        
    
    # ajax validation
    (r"^validate/$", "ajax_validation.views.validate", {
        "form_class": FeatureForm,
        "callback": lambda request, *args, **kwargs: {"user": request.user}
    }, "blog_form_validate"),
)
