from django.urls import path
from .views import item_detail, buy_item, order_detail, buy_order, success, cancel

urlpatterns = [
    path("item/<int:id>/", item_detail),
    path("buy/<int:id>/", buy_item),
    path("order/<int:id>/", order_detail),
    path("buy/order/<int:id>/", buy_order),
    path("success/", success),
    path("cancel/", cancel),
]
