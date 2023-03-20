
from django.urls import path

from .views import DealTypeApiView

urlpatterns = [
    path('manage', DealTypeApiView.as_view())
]