"""mynt_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include("mynt_users.urls")),
    path('api/investor-consent/',include("investor_consent.urls")),
    path('api/investor-kyc/',include("investor_kyc.urls")),
    path('api/company/',include("company.urls")),
    path('api/campaign/',include("campaign.urls")),
    path('api/deal_type/',include("deal_type.urls")),
    path('api/faqs/',include("faqs.urls")),
    path('api/highlights/',include("highlights.urls")),
    path('api/people/',include("people.urls")),
    path('api/press/',include("press.urls")),
    path('api/rewards/',include("rewards.urls")),
    path('api/deal_terms/',include("deal_terms.urls")),
    path('api/documents/',include("documents.urls")),
    path('api/payments/',include("payment.urls"))
]

urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)