from django.urls import path, include
from .views import *
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.profile, name='home'),  

    path('accounts/', include('allauth.urls')),

    path('login/', RedirectView.as_view(url='/accounts/login/')),
    path('register/', RedirectView.as_view(url='/accounts/signup/')),
    path('logout/', RedirectView.as_view(url='/accounts/logout/')),
    path('password/change/', RedirectView.as_view(url='/password/change/')),
    path('password/reset/', RedirectView.as_view(url='/password/reset/')),

    path('profile/', views.profile, name='profile'),
    
    path('api/camps/create/', CreateCampAPI.as_view(), name='api_create_camp'),
    path('register-camper-page/', views.register_camper_page, name='register_camper_page'),
    path('api/register-camper/', RegisterCamperAPI.as_view(), name='api_register_camper'),
    path('my-camper/', views.my_campers, name='my_camper'),
    path('api/mycamper/', CampersView.as_view(), name='api_mycamper'),
]