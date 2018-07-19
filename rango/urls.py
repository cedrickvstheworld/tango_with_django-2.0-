from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<category_name_url>/', views.category, name='category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<category_name_url>/add_pages/', views.add_pages, name='add_pages'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('goto/', views.track_url, name='track_url'),
    path('like/', views.category_like, name='like'),
    path('search/', views.search, name='search'),
    path('categorysearch/', views.categorysearch, name='categorysearch')
]
