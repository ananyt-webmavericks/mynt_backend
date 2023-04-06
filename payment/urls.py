from django.urls import path

from  .views import CreateOrder,GetOrderDetails,SuccessWebhook
urlpatterns = [
    path('create-order', CreateOrder.as_view()),
    path('get/order-details/<str:order_id>', GetOrderDetails.as_view()),
    path('webhook', SuccessWebhook.as_view())
]