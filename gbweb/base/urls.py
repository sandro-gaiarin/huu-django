from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name='home'),
    path('coderoom/<str:pk>/', views.coderoom, name="coderoom"),
    path('create-coderoom/', views.createCodeRoom, name="create-coderoom"),
    path('update-coderoom/<str:pk>/',
         views.updateCodeRoom, name="update-coderoom"),
    path('delete-coderoom/<str:pk>/',
         views.deleteCodeRoom, name="delete-coderoom"),

    #path ('upload/', views.upload, name = 'upload'),

]
