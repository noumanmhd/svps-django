
from django.urls import path
from .views import (
    home,
    profile,
    fresh_login,
    reserve,
    SlotsListView
)

urlpatterns = [
    path('', home, name='home'),
    path(r'profile', profile, name='profile'),
    path(r'book', SlotsListView.as_view(), name='book'),
    path(r'reserve/<int:pk>', reserve, name='reserve'),
    path(r'fresh-login', fresh_login, name='fresh-login')
]
