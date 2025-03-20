from django.urls import path
from .views import PostListView, PostCreateView, PostDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]