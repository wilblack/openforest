from django.shortcuts import render_to_response
from features.models import Feature
from django.template import RequestContext
import json

def home(request):
    features = Feature.objects.filter(feature_of__isnull=True)[0:5]
    features_json = [f.json for f in features]
    for i,f in enumerate(features):
        html = render_to_response("features/infowindow.html",
                                  {"feature":f},
                                  context_instance=RequestContext(request),
                                  ).content
        features_json[i]["html"]=html
    
    
    tv = {'features':features,
          'features_json':json.dumps(features_json)}
    return render_to_response('homepage.html',tv, context_instance=RequestContext(request))
