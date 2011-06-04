# -*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe



register = template.Library()
@register.inclusion_tag("features/feature_item.html")
def show_feature(blog_post):
    return {"blog_post": blog_post}


@register.inclusion_tag("features/feature_item.html")
def show_project(blog_post, features):
    return {"blog_post": blog_post,
            "features":features}

@register.inclusion_tag("features/meta.html")
def show_feature_meta(blog_post):
    return {"blog_post": blog_post}

#@register.inclusion_tag("features/feature_item.html")
#def show_blog_post(blog_post):
#    return {"blog_post": blog_post}