from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo.views.TodoView import ToDoListCreate, ToDoDetail

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path('todo/', ToDoListCreate.as_view(), name='todo-list-create'),
    path('todo/<int:pk>/', ToDoDetail.as_view(), name='todo-detail'),
]
