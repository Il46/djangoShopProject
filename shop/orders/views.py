from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Order


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/my_orders.html", {"orders": orders})
