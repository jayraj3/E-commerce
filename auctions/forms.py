from django.forms import ModelForm
from .models import CreateAdd


class CreateAddForm(ModelForm):
    class Meta:
        model = CreateAdd
        fields = ['item_name', 'price', 'image']
