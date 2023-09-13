
from django.urls import path

from interest.views import CreateInterest,CheckInterest,GetAllInterest

urlpatterns = [
    path('create-interest', CreateInterest.as_view()),
    path('check-interest/<int:user_id>/<int:campaign_id>', CheckInterest.as_view()),
    path('admin-get-all-interests', GetAllInterest.as_view())
]