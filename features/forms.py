from datetime import datetime
from features.models import FeatureType

from django import forms
from django.utils.translation import ugettext_lazy as _

from features.models import Feature

class FeatureForm(forms.ModelForm):
    from django.template.defaultfilters import slugify
        
    slug = forms.SlugField(widget=forms.HiddenInput())
    #    max_length = 20,
    #    help_text = _("a short version of the title consisting only of letters, numbers, underscores and hyphens."),
    #)
    
    #geom = forms.CharField(widget=forms.HiddenInput())
    geomtype = forms.CharField(widget=forms.HiddenInput())
    featuretype = forms.CharField(widget=forms.HiddenInput())
    #tease = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Feature
        exclude = [
            "author",
            "creator_ip",
            "created_at",
            "updated_at",
            "publish",
            "allow_comments",
            "photoset",
            "markup",
            "tease",
            "barcode"
            
            
        ]
        
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(FeatureForm, self).__init__(*args, **kwargs)
    
    def clean_featuretype(self):
        data = self.cleaned_data['featuretype']
        return FeatureType.objects.get(pk=data)
    
    
    def clean_slug(self):
        if not self.instance.pk:
            if Feature.objects.filter(author=self.user, created_at__month=datetime.now().month, created_at__year=datetime.now().year, slug=self.cleaned_data["slug"]).exists():
                raise forms.ValidationError(u"This field must be unique for username, year, and month")
            return self.cleaned_data["slug"]
        try:
            post = Feature.objects.get(
                author = self.user,
                created_at__month = self.instance.created_at.month,
                created_at__year = self.instance.created_at.year,
                slug = self.cleaned_data["slug"]
            )
            if post != self.instance:
                raise forms.ValidationError(u"This field must be unique for username, year, and month")
        except Feature.DoesNotExist:
            pass
        return self.cleaned_data["slug"]
