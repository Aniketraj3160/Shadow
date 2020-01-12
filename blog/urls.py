from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing-page'),
    path('blog/home/', PostListView, name='blog-home'),
    path('blog/home/<int:check>/', views.PostListView_Auth, name='blog-home-authority'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('registerCamera/', views.RegisterCamera, name='register-camera'),
    path('post/<int:pk>/comment/', views.add_comment_to_post,
         name='add_comment_to_post'),
    
    path('posttt/<int:pk>/approve/',
         views.post_approve, name='post_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('like/', views.upvote_post, name='upvote_post'),

    ######################################################################################################################################################
    #EDIT STARTS#
    ######################################################################################################################################################

    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('invalid/', views.invalid, name='invalid_page'),

    ######################################################################################################################################################
    #EDIT STOPS#
    ######################################################################################################################################################


    path('dislike/', views.downvote_post, name='downvote_post'),
    path('graphs/', views.linkgraph, name='linkgraph'),
    path('graphs/india', views.indianmap, name='indianmap'),
    path('graphs/line', views.linegraph, name='linegraph'),
    path('graphs/pie', views.piechart, name="piechart"),
    path('graphs/donut', views.donut, name="donut"),
    path('cameralist/', views.cameraslist, name='cameraslist'),
    path('api', views.post_rest.as_view(), name='api'),
    path('trending/', views.post_ordered_by_upvotes, name='trend'),
    path('trending/monthly', views.post_ordered_by_upvotes_monthly, name='monthly-trend'),

]
