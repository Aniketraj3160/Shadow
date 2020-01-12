from django.urls import path, include, re_path
from . import views
from .views import *
from rest_framework import routers


# router = routers.DefaultRouter()
#p = re_path(r'^posts/(?P<city>\w+)/$', views.post_list, name='city'),
#p = url('^posts/(?P<city>.+)/$', post_list.as_view())
#router.register('posts/<city>/', views.post_list)
# router.register(p)
# router.register('cameras', views.camera_list)

router = routers.DefaultRouter()
#router.register('postings', views.post_list1)
#router.register('cameras', views.camera_list1)
#router.register('authority', views.authority_list)
#router.register('journalist', views.journalist_list)
urlpatterns = [
    # path('api1', views.api, name='api'),
    # path('rest/cameras/', views.camera_list, name='camera_list'),
    path("rest/post/<str:city>", views.post_list.as_view(), name="results_api"),
    path("rest/posts/", views.post_list1.as_view(), name="results_api"),
    path("rest/cameras/", views.camera_list1.as_view(), name="results_api"),
    path("rest/authority/", views.authority_list.as_view(), name="results_api"),
    path("rest/journalist/", views.journalist_list.as_view(), name="results_api"),

    path("rest/camera/<str:city>",
         views.camera_list.as_view(), name="results_api"),
    #path('rest/', include(router.urls)),

    # path('rest/', include(router.urls)),

]
