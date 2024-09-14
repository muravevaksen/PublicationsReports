from django.forms import ModelForm
from .models import Publication as PublicationModel
from .models import Author as AuthorModel
from .models import Journal as JournalModel
from .models import Departament as DepartModel

class PublicationForm(ModelForm):
    class Meta:
        model = PublicationModel
        fields = "__all__"


class AuthorForm(ModelForm):
    class Meta:
        model = AuthorModel
        fields = "__all__"


class JournalForm(ModelForm):
    class Meta:
        model = JournalModel
        fields = "__all__"

class DepartForm(ModelForm):
    class Meta:
        model = DepartModel
        fields = "__all__"
