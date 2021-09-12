from django.forms import ModelForm
from .models import Item
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,  Submit,Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method= 'post'
        self.helper.add_input(Submit('submit', 'Submit'))