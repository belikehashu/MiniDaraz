from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('review/<int:review_id>/edit/', views.edit_review_view, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review_view, name='delete_review'),

]
