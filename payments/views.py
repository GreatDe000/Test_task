import stripe
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Item, Order


def item_detail(request, id: int):
    item = Item.objects.filter(id=id).first()
    if item is None:
        return HttpResponse("Item not found")

    return render(
        request,
        "payments/item_detail.html",
        {
            "item": item,
            "price_display": f"{item.price / 100:.2f}",
            "stripe_pk": settings.STRIPE_PUBLISHABLE_KEY,
        }
    )


def buy_item(request, id: int):
    item = Item.objects.filter(id=id).first()
    if item is None:
        return JsonResponse({"error": "Item not found"})

    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.name,
                    "description": item.description[:5000],
                },
                "unit_amount": item.price,
            },
            "quantity": 1,
        }],
        success_url=f"{settings.DOMAIN}/success/",
        cancel_url=f"{settings.DOMAIN}/cancel/",
    )

    return JsonResponse({"session_id": session.id})

def order_detail(request, id: int):
    order = Order.objects.filter(id=id).first()
    if order is None:
        return HttpResponse("Order not found")

    order_items = order.items.select_related("item").all()
    total_display = f"{order.total_price() / 100:.2f}"

    return render(
        request,
        "payments/order_detail.html",
        {
            "order": order,
            "order_items": order_items,
            "total_display": total_display,
            "stripe_pk": settings.STRIPE_PUBLISHABLE_KEY,
        }
    )


def buy_order(request, id: int):
    order = Order.objects.filter(id=id).first()
    if order is None:
        return JsonResponse({"error": "Order not found"})

    stripe.api_key = settings.STRIPE_SECRET_KEY

    order_items = order.items.select_related("item").all()
    if not order_items:
        return JsonResponse({"error": "Order is empty"})

    line_items = []
    for oi in order_items:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": oi.item.name},
                "unit_amount": oi.item.price,
            },
            "quantity": oi.quantity,
        })

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=line_items,
        success_url=f"{settings.DOMAIN}/success/",
        cancel_url=f"{settings.DOMAIN}/cancel/",
    )

    return JsonResponse({"session_id": session.id})


def success(request):
    return HttpResponse("Payment success")


def cancel(request):
    return HttpResponse("Payment cancelled")