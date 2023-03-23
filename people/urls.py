from django.urls import path

from .views import PeopleApiView

urlpatterns = [
    path('manage', PeopleApiView.as_view()),
]