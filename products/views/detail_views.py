from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from orders.models.order_item import OrderItem
from products.models.product import Product
from products.models.product_review import ProductReview
from products.forms import ProductReviewForm
from products.services.review_service import save_review

@login_required
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = ProductReview.objects.filter(product=product).order_by("-created_at")

    has_purchased = OrderItem.objects.filter(
        product=product,
        order__user=request.user,
        order__status='Delivered'
    ).exists()

    existing_review = ProductReview.objects.filter(user=request.user, product=product).first()
    form = None

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if has_purchased and not existing_review:
            form = ProductReviewForm(request.POST)
            if form.is_valid():
                new_review = save_review(form, request.user, product)
                return JsonResponse({
                    'success': True,
                    'review_html': render_to_string('products/_single_review.html', {
                        'review': new_review,
                        'user': request.user
                    }, request=request)
                })
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    elif not existing_review:
        form = ProductReviewForm()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'has_purchased': has_purchased,
        'existing_review': existing_review,
    })
