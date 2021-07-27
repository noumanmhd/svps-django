
from django.urls import path
from .views import (
    home,
    profile,
    fresh_login,
    reserve,
    release,
    update_state,
    check_plate,
    SlotsListView
)

urlpatterns = [
    path('', home, name='home'),
    path(r'profile', profile, name='profile'),
    path(r'book', SlotsListView.as_view(), name='book'),
    path(r'reserve/<int:pk>', reserve, name='reserve'),
    path(r'release/<int:pk>', release, name='release'),
    path(r'update-state/', update_state, name='update-state'),
    path(r'check-plate/', check_plate, name='check-plate'),
    path(r'fresh-login', fresh_login, name='fresh-login')
]
