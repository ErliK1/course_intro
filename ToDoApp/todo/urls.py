from django.urls import path
from todo.views.todo_views import  create_task_api_view, get_task_api_view, \
                                    TaskGetForUserAPIView, TaskRetrieveAPIView, UserListCreateAPIView, TaskForUser 


urlpatterns = [
        path('task/list/', get_task_api_view, name="get-task"),
        path('task/create/', create_task_api_view, name="create-task"),
        path('task/for/user/<int:user_id>/', TaskGetForUserAPIView.as_view(), name="task-for-user"),
        path('task/retrieve/<int:pk>/', TaskRetrieveAPIView.as_view(), name="retrieve-task"),
        path('user/list/create/', UserListCreateAPIView.as_view(), name='list-create-user'), 
        path("user/tasks/", TaskForUser.as_view(), name='user-task'),
]
