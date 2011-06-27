import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic import date_based

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from simplejson import dumps as json
from features.models import Post, Feature, FeatureType
from pinax.apps.photos.models import PhotoSet
from features.forms import *
from threadedcomments.models import FreeThreadedComment

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
try:
    from friends.models import Friendship
    friends = True
except ImportError:
    friends = False



def features(request, username=None, template_name="features/features.html"):
    ''' This view is a list of features. If user is authenticated they get all their features. 
        If the user is not logged in they all features. 
    '''
    blogs = Feature.objects.filter(status=2, feature_of__isnull=True).order_by("-publish")
    if username is not None:
        user = get_object_or_404(User, username=username.lower())
        blogs = blogs.filter(author=user)
    return render_to_response(template_name, {
        "features": blogs,
    }, context_instance=RequestContext(request))


def post(request, username, year, month, slug,
         template_name="features/post.html"):
    
    ''' The main Project and Feature view'''
    post = Feature.objects.filter(
        slug = slug,
        publish__year = int(year),
        publish__month = int(month),
        author__username = username,
        #feature_of__isnull=True,
    )
    
    if not post:
        raise Http404
    
    if post[0].status == 1 and post[0].author != request.user:
        raise Http404
    
    features = post[0].feature_set.all()
    features = post | features 
        
    featureList=[f.json for f in features]
        
    for i,f in enumerate(features):
        html = render_to_response("features/infowindow.html",{"feature":f}).content
        featureList[i]["html"]=html
    
        
    return render_to_response(template_name, {
        "post": post[0],
        "features":json(featureList),
        "free_threaded_comments": FreeThreadedComment.objects.filter(name='Android',object_id=post[0].id)
    }, context_instance=RequestContext(request))


def feature(request, username, year, month, slug,
         template_name="features/post.html"):
    post = Feature.objects.filter(
        slug = slug,
        publish__year = int(year),
        publish__month = int(month),
        author__username = username,
        feature_of__isnull=False,
    )
    
    if not post:
        raise Http404
    
    if post[0].status == 1 and post[0].author != request.user:
        raise Http404
    
    return render_to_response(template_name, {
        "post": post[0],
        "project":post[0].feature_of
    }, context_instance=RequestContext(request))


@login_required
def your_posts(request, template_name="features/your_posts.html"):
    return render_to_response(template_name, {
        "blogs": Feature.objects.filter(author=request.user, feature_of__isnull=True),
    }, context_instance=RequestContext(request))


@login_required
def destroy(request, id):
    post = Feature.objects.get(pk=id)
    user = request.user
    title = post.title
    if post.author != request.user:
        messages.add_message(request, messages.ERROR,
            ugettext("You can't delete features that aren't yours")
        )
        return HttpResponseRedirect(reverse("feature_list_yours"))
    
    if request.method == "POST" and request.POST["action"] == "delete":
        post.delete()
        messages.add_message(request, messages.SUCCESS,
            ugettext("Successfully deleted feature '%s'") % title
        )
        return HttpResponseRedirect(reverse("feature_list_yours"))
    else:
        return HttpResponseRedirect(reverse("feature_list_yours"))
    
    return render_to_response(context_instance=RequestContext(request))


@login_required
def new(request, form_class=FeatureForm, template_name="features/new.html"):
    if request.method == "POST":
        if request.POST["action"] == "create":
            blog_form = form_class(request.user, request.POST)
            if blog_form.is_valid():
                blog = blog_form.save(commit=False)
                blog.author = request.user
                if getattr(settings, 'BEHIND_PROXY', False):
                    blog.creator_ip = request.META["HTTP_X_FORWARDED_FOR"]
                else:
                    blog.creator_ip = request.META['REMOTE_ADDR']
                blog.save()
                ps = PhotoSet(name=request.POST['slug'])
                ps.description = request.POST['title']+" photoset"
                ps.save()               
                blog.photoset=ps
                blog.save()
                # @@@ should message be different if published?
                messages.add_message(request, messages.SUCCESS,
                    ugettext("Successfully saved project '%s'") % blog.title
                )
                if notification:
                    if blog.status == 2: # published
                        if friends: # @@@ might be worth having a shortcut for sending to all friends
                            notification.send((x['friend'] for x in Friendship.objects.friends_for_user(blog.author)), "blog_friend_post", {"post": blog})
                
                return HttpResponseRedirect(reverse("feature_list_yours"))
        else:
            blog_form = form_class()
    else:
        blog_form = form_class()
    
    return render_to_response(template_name, {
        "blog_form": blog_form,
        'featureType':FeatureType.objects.all()
    }, context_instance=RequestContext(request))


@login_required
def edit(request, id, form_class=FeatureForm, template_name="features/edit.html"):
    post = get_object_or_404(Feature, id=id)
    
    if request.method == "POST":
        if post.author != request.user:
            messages.add_message(request, messages.ERROR,
                ugettext("You can't edit posts that aren't yours")
            )
            return HttpResponseRedirect(reverse("feature_list_yours"))
        if request.POST["action"] == "update":
            blog_form = form_class(request.user, request.POST, instance=post)
            if blog_form.is_valid():
                blog = blog_form.save(commit=False)
                blog.save()
                messages.add_message(request, messages.SUCCESS,
                    ugettext("Successfully updated project '%s'") % blog.title
                )
                if notification:
                    if blog.status == 2: # published
                        if friends: # @@@ might be worth having a shortcut for sending to all friends
                            notification.send((x['friend'] for x in Friendship.objects.friends_for_user(blog.author)), "blog_friend_post", {"post": blog})
                
                return HttpResponseRedirect(reverse("feature_list_yours"))
        else:
            blog_form = form_class(instance=post)
    else:
        blog_form = form_class(instance=post)
    
    return render_to_response(template_name, {
        "blog_form": blog_form,
        "post": post,
    }, context_instance=RequestContext(request))

def list(request):
    
    features = Feature.objects.filter(feature_of__isnull=True)
    out = [{'title':f.title, 'fid':f.id} for f in features]
        
    if 'callback' in request.GET:
        out = request.GET['callback']+"("+json+")"        
    else: 
        out=json(out)
    return HttpResponse(out)
    
def update(request):
    post = request.POST
    fid=post['fid']
    photos = post['data']['photos']
    f = get_object_or_404(Feature, id=id)
       
    



