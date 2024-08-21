from django.forms import ModelForm
from .models import Publication as PublicationModel

class PublicationForm(ModelForm):
    class Meta:
        model = PublicationModel
        fields = "__all__"