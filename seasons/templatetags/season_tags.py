from django import template
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from seasons.models import Season
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_season(d, autoescape=None):
    text =  Season.objects.get_season(d).name
    color = Season.objects.get_season(d).color
    result = "<span style='color:#FFFFFF; background:%s; padding:0px 3px 0px 3px; '>"%color
    
    result += "<strong> %s </strong> </span>" %(text)
    return mark_safe(result)
get_season.needs_autoescape = True

@register.tag(name="season_color")
def do_season_color(parser, token):
     
     return season_color(token)


class season_color(template.Node):
    def __init__(self, value):
            self.value=value

    def render(self, context):
        color='gray'
        text= self.value
        #color = Season.objects.get_season(self.value).color
        #text = Season.objects.get_season(self.value).name
        return "<span style='color:#000000; background:%s;'>%s</span>" %(color, text)
    
