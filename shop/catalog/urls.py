from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("categories/", views.category_list, name="category_list"),
    path("category/<slug:slug>/", views.product_list_by_category, name="product_list_by_category"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("add-to-cart/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("remove-from-cart/<slug:slug>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
]