from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from todo.models import DailyUser, DailyTask
from todo.serializers.todo_serializers import UserSerializer, TaskCreateSerializer, TaskGetSerializer, UserGetTaskSerializer


class UserListCreateAPIView(ListCreateAPIView):
    queryset = DailyUser.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
def create_task_api_view(request: Request, *args, **kwargs) -> Response:
    data = request.data
    serializer = TaskCreateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_task_api_view(request: Request, *args, **kwargs) -> Response:
    tasks = DailyTask.objects.all()
    serializer = TaskGetSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class TaskGetForUserAPIView(ListAPIView):
    queryset = DailyTask.objects.all()
    serializer_class = TaskGetSerializer

    def get_queryset(self, ):
        id_of_user = self.kwargs.get('user_id')
        if id_of_user:
            return DailyTask.objects.filter(daily_user__pk=id_of_user)
        return DailyTask.objects.none()


class TaskRetrieveAPIView(RetrieveAPIView):
    queryset = DailyTask.objects.all()
    serializer_class = TaskGetSerializer

    def get_object(self, ):
        queryset = DailyTask.objects.filter(pk=self.kwargs('pk'))
        if not queryset.exists():
            raise Http404
        return queryset.first()

class TaskForUser(ListAPIView):
    queryset = DailyUser.objects.all()
    serializer_class = UserGetTaskSerializer


