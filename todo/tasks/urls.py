from django.urls import path
from . import views
from .views import CustomLoginView, ListTask, UpdateTask, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(redirect_authenticated_user=True), name='register'),
    

    
    path('', ListTask.as_view(), name ="list"),
    path('update_task/<str:pk>', UpdateTask.as_view(), name="update_task"),
    path('delete_task/<str:pk>', views.deleteTask, name="delete"),


]
