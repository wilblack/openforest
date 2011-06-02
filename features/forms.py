from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from features.models import Feature



class FeatureForm(forms.ModelForm):
    
    slug = forms.SlugField(
        max_length = 20,
        help_text = _("a short version of the title consisting only of letters, numbers, underscores and hyphens."),
    )
    
    class Meta:
        model = Feature
        exclude = [
            "author",
            "creator_ip",
            "created_at",
            "updated_at",
            "publish",
            "allow_comments"
        ]
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(FeatureForm, self).__init__(*args, **kwargs)
    
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
