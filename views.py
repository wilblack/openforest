from django.shortcuts import render_to_response
from features.models import Feature
from django.template import RequestContext

def home(request):
    features = Feature.objects.filter().reverse()[0:5]
    
    tv = {'features':features}
    return render_to_response('homepage.html',tv, context_instance=RequestContext(request))