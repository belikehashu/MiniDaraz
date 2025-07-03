from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, ProductReview
from django.core.paginator import Paginator
from .forms import ProductReviewForm
from django.contrib.auth.decorators import login_required
from orders.models import OrderItem
from django.contrib import messages 

def index_view(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    sort = request.GET.get('sort')

    products = Product.objects.filter(stock__gt=0)

    if query:
        products = products.filter(name__icontains=query)

    if category_id and category_id != "all":
        products = products.filter(category_id=category_id)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_az':
        products = products.order_by('name')
    elif sort == 'name_za':
        products = products.order_by('-name')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'products/index.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'search_query': query,
        'sort': sort
    })

@login_required
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = ProductReview.objects.filter(product=product).order_by("-created_at")

    has_purchased = OrderItem.objects.filter(
        product=product,
        order__user=request.user,
        order__status='Delivered'
    ).exists()

    if request.method == 'POST' and has_purchased:
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']

            review, created = ProductReview.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={
                    'rating': rating,
                    'comment': comment,
                }
            )
            messages.success(request, "Review submitted successfully.")
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, "There was an error with your review.")
    else:
        form = ProductReviewForm()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'has_purchased': has_purchased,
    })

@login_required
def edit_review_view(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id, user=request.user)

    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated.")
            return redirect('product_detail', product_id=review.product.id)
    else:
        form = ProductReviewForm(instance=review)

    return render(request, 'products/edit_review.html', {'form': form})

@login_required
def delete_review_view(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id, user=request.user)
    product_id = review.product.id
    review.delete()
    messages.success(request, "Review deleted.")
    return redirect('product_detail', product_id=product_id)
