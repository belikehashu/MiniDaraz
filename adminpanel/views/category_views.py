from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from products.models.category import Category
from products.forms import CategoryForm
from adminpanel.services.category_service import delete_category_by_id

def is_superadmin(user):
    return user.is_superuser

@user_passes_test(is_superadmin)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'adminpanel/categories.html', {'categories': categories})

@user_passes_test(is_superadmin)
def add_edit_category(request, category_id=None):
    category = get_object_or_404(Category, id=category_id) if category_id else None
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'adminpanel/add_edit_category.html', {'form': form})

@user_passes_test(is_superadmin)
def delete_category(request, category_id):
    delete_category_by_id(category_id)
    return redirect('admin_categories')
