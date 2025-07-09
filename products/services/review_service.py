def save_review(form, user, product):
    review = form.save(commit=False)
    review.user = user
    review.product = product
    review.save()
    return review
