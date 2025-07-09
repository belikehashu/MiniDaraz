from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('review/edit/<int:review_id>/ajax/', views.edit_review_ajax, name='edit_review_ajax'),
    path('review/delete/<int:review_id>/ajax/', views.delete_review_ajax, name='delete_review_ajax'),
]
