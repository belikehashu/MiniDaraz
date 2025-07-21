from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('products.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('notifications/', include('notifications.urls')),
    path('brandpanel/', include('brandpanel.urls')),
    path('managerpanel/', include('managerpanel.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
