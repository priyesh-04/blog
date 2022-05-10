
from django.urls import path
from .views import (
                    PostListView, 
					PostDetailView, 
					PostCreateView, 
					PostUpdateView, 
					PostDeleteView)

urlpatterns = [
    path('', PostListView.as_view(), name='list-view'),
    path('create/', PostCreateView.as_view(), name='create-view'),
    path('<slug>/update', PostUpdateView.as_view(), name='update-view'),
    path('<slug>/delete', PostDeleteView.as_view(), name='delete-view'),
    path('<slug>/', PostDetailView.as_view(), name='detail-view'),
]
