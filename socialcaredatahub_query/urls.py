from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('search/',views.search,name = 'search'),
    path('results/',views.results,name='results'),
    path('download_excel/',views.download_excel,name = 'download excel')
]