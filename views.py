from django.shortcuts import render_to_response
from features.models import Feature
from django.template import RequestContext
import json

def home(request):
    features = Feature.objects.all().order_by("-updated_at")[0:6]
    
    features_json = [f.json for f in features]
    myFeatures = []
    user = request.user.is_authenticated()
    if request.user.is_authenticated():
        myFeatures = Feature.objects.filter(feature_of__isnull=True, author=request.user)
    
    for i,f in enumerate(features):
        html = render_to_response("features/infowindow.html",
                                  {"feature":f},
                                  context_instance=RequestContext(request),
                                  ).content
        features_json[i]["html"]=html
        
    tv = {'features':features,
          'myFeatures':myFeatures,
          'features_json':json.dumps(features_json)}
    return render_to_response('homepage.html',tv, context_instance=RequestContext(request))
