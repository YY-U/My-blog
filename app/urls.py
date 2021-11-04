from django.urls import path
from app import views

urlpatterns=[
    path('',views.IndexView.as_view(),name='index'),
    path('post/<int:pk>',views.PostDetailView.as_view(),name='post_detail'),
    #<int:pk>投稿のID(数字)，どの投稿の詳細か区別
    path('post/new/',views.CreatePostView.as_view(),name='post_new'),#新規投稿url
    path('post/<int:pk>/edit/',views.PostEditView.as_view(),name='post_edit'),
    path('post/<int:pk>/delete/',views.PostDeleteView.as_view(),name='post_delete'),
]