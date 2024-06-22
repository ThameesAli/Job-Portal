from django.forms import ModelForm
from .models import *

class ApplyForm(ModelForm):
    class Meta:
        model=Candidate
        fields="__all__"