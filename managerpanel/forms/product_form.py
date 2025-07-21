from django import forms
from products.models.product import Product
from products.models.category import Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1499'}),
                'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock quantity'}),
                'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        branch = kwargs.pop('branch', None)  # branch ko kwargs se uthao
        super().__init__(*args, **kwargs)

        # Branch pass hua ho to uski categories filter karo
        if branch:
            self.fields['category'].queryset = Category.objects.filter(branch=branch)

        # Hide branch field if it exists
        if 'branch' in self.fields:
            self.fields['branch'].widget = forms.HiddenInput()
