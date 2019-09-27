from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('ticket/<int:ticket_id>/', views.ticket, name='ticket'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
