from django.urls import path

from . import views

urlpatterns = [path('',views.home,name='home'),
               path('register/', views.register, name='register'),
               path('login/', views.login, name='login'),
               path('upload/', views.uploadfunc, name='upload'),
               path('delete_dataset/', views.deleteuploaded, name='deleteuploaded'),
               path('logout/', views.logout, name='logout'),
               path('remove_duplicates/', views.removedup, name='removedup'),
               path('analyse/', views.analyse, name='analyse'),
               path('rename/', views.rename, name='rename'),
               path('view_uploaded/', views.viewuploaded, name='viewuploaded'),
               path('clean_data/', views.clean, name='clean_data'),
               path('user_dashboard/', views.user_dashboard, name='user_dashboard')
               ]