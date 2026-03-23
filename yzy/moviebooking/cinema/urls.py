from django.urls import path
from . import views

urlpatterns = [

path('', views.home),

path('movie/<int:id>/', views.movie_detail, name='movie_detail'),

path('seat/<int:id>/', views.seat),

path('payment/<int:id>/', views.payment),

path('ticket/<int:id>/',views.ticket),

path('mytickets/',views.mytickets),

# admin panel

path('admin-dashboard/', views.admin_dashboard),

path('add-movie/', views.add_movie),

path('edit-movie/<int:id>/', views.edit_movie),

path('delete-movie/<int:id>/', views.delete_movie),

path('login/', views.login_user),

path('logout/', views.logout_user),

]