from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('post-login/', views.after_login, name='after_login'),
    path('profile-page/', views.profile_page, name='profile_page'),
    url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='activate'),
    path('userprofile/<int:pk>/', views.userprofile, name='userprofile'),
    path('userprofile1/<int:pk>/', views.userprofile1, name='userprofile1'),

]
