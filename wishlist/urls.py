from django.urls import path
from wishlist.views.wishlist_views import wishlist_view
from wishlist.views.wishlist_views import add_to_wishlist
from wishlist.views.wishlist_views import remove_from_wishlist

urlpatterns = [
    path('', wishlist_view, name='wishlist'),
    path('add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
