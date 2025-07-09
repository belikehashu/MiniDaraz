from products.models.category import Category
from django.shortcuts import get_object_or_404

def delete_category_by_id(category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
