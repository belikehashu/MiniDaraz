from django import forms
from .models import Product, Category, ProductReview

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

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }