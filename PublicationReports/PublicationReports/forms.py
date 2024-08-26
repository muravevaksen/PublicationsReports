from django.forms import ModelForm
from .models import Publication as PublicationModel
from .models import Author as AuthorModel

class PublicationForm(ModelForm):
    class Meta:
        model = PublicationModel
        fields = "__all__"

class AuthorForm(ModelForm):
     class Meta:
         model = AuthorModel
         fields = "__all__"