from django.urls import path

from .views import DocumentsApiView

urlpatterns = [
    path('manage', DocumentsApiView.as_view()),
]