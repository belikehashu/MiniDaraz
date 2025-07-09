from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from products.models.product_review import ProductReview
from products.forms import ProductReviewForm

@login_required
def edit_review_ajax(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id, user=request.user)

    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if request.method == 'GET':
        form = ProductReviewForm(instance=review)
        html = render_to_string('products/_edit_review_form.html', {'form': form, 'review': review}, request=request)
        return JsonResponse({'form_html': html})

    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            html = render_to_string('products/_single_review.html', {'review': review, 'user': request.user}, request=request)
            return JsonResponse({'success': True, 'review_html': html})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@login_required
def delete_review_ajax(request, review_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            review = ProductReview.objects.get(id=review_id, user=request.user)
            review.delete()
            return JsonResponse({'success': True})
        except ProductReview.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Review not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
