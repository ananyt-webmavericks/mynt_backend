from django.urls import path

from  .views import CreateOrder,GetOrderDetails,SuccessWebhook, GetAllPaymentDetails, InvestorPaymentDetailApiView,OfflinePaymentDetails,UpdateOfflinePaymentDetails
urlpatterns = [
    path('create-order', CreateOrder.as_view()),
    path('get/order-details/<str:order_id>', GetOrderDetails.as_view()),
    path('webhook', SuccessWebhook.as_view()),
    path('get-all-payment-details', GetAllPaymentDetails.as_view()),
    path('investor-payment-details-by-user-id/<int:user_id>', InvestorPaymentDetailApiView.as_view()),
    path('make-offline-payment', OfflinePaymentDetails.as_view()),
    path('update-offline-payment/admin/<int:payment_id>',UpdateOfflinePaymentDetails.as_view())
]