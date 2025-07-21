from django import forms
from products.models.product import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'price': forms.NumberInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'description': forms.Textarea(attrs={'style': 'width: 100%; padding: 10px;'}),
            'image': forms.ClearableFileInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'stock': forms.NumberInput(attrs={'style': 'width: 100%; padding: 10px;'}),
        }
