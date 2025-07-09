from django.contrib import admin
from .models.category import Category
from .models.product import Product
from .models.product_review import ProductReview
from .models.product_image import ProductImage


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductReview)