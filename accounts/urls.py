from django.urls import path
from django.contrib import admin


from accounts.views import (register_view,
							login_view,
							# RegisterView,
							logout_view,
							)

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path('register/', register_view, name='register'),
	path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]