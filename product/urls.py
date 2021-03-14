from django.contrib import admin
from django.urls import path, include
from product.views import ProductView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('/main', ProductView.as_view()),
    path('/update/<int:product_id>', ProductUpdateView.as_view()),
    path('/delete/<int:product_id>', ProductDeleteView.as_view()),
]