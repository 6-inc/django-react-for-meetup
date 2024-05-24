from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo.views.TodoView import TodoListCreate, TodoDetail

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path('todo/', TodoListCreate.as_view(), name='todo-list-create'),
    path('todo/<int:pk>/', TodoDetail.as_view(), name='todo-detail'),
]
