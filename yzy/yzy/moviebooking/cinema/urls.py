from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

path('', views.home, name='home'),

path('movie/<int:id>/', views.movie_detail, name='movie_detail'),

path('seat/<int:id>/', views.seat, name='seat'),

path('payment/<int:id>/', views.payment, name='payment'),

path('ticket/<int:id>/',views.ticket),

path('mytickets/', views.mytickets, name='mytickets'),

path('favorite/<int:id>/', views.add_favorite, name='favorite'),

path('favorites/', views.my_favorites, name='favorites'),

path('rate/<int:id>/', views.rate_movie, name='rate_movie'),



# admin panel

path('admin-dashboard/', views.admin_dashboard),

path('users/', views.admin_users, name='admin_users'),

path('add-movie/', views.add_movie),

path('edit-movie/<int:id>/', views.edit_movie),

path('delete-movie/<int:id>/', views.delete_movie, name='delete_movie'),

path('register/', views.register, name='register'),

path('login/', views.login_view, name='login'),

path('logout/', views.logout_view, name='logout'),

path('add-user/', views.add_user, name='add_user'),

path('edit-user/<int:id>/', views.edit_user, name='edit_user'),

path('delete-user/<int:id>/', views.delete_user, name='delete_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
