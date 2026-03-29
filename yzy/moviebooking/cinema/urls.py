from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

path('', views.home, name='home'),

path('movie/<int:id>/', views.movie_detail, name='movie_detail'),

path('seat/<int:id>/', views.seat, name='seat'),

path('payment/<int:id>/', views.payment),

path('ticket/<int:id>/',views.ticket),

path('mytickets/',views.mytickets),

path('favorite/<int:id>/', views.add_favorite, name='favorite'),

path('favorite/<int:id>/', views.favorite, name='favorite'),

path('favorites/', views.my_favorites, name='favorites'),

path('rate/<int:id>/', views.rate_movie, name='rate_movie'),



# admin panel

path('admin-dashboard/', views.admin_dashboard),

path('add-movie/', views.add_movie),

path('edit-movie/<int:id>/', views.edit_movie),

path('delete-movie/<int:id>/', views.delete_movie),

path('login/', views.login_view, name='login'),

path('register/', views.register_view, name='register'),

path('logout/', views.logout_view, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)