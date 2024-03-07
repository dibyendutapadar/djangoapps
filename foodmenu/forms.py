from django.forms import ModelForm
from .models import Item

class AddItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item_name','item_desc','item_price']


