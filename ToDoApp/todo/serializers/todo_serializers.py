from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from todo.models import DailyTask, DailyUser

from django.utils import timezone


class TaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    due_to = serializers.DateTimeField()
    daily_user = serializers.PrimaryKeyRelatedField(queryset=DailyUser.objects.all())

    def validate_due_to(self, value):
        now_time = timezone.now()
        if now_time > value:
            raise ValidationError("Please add a date in the future")
        return value

    def create(self, validated_data):
        obj = DailyTask(**validated_data)
        obj.save()
        print("YEAH")
        return obj


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyUser
        fields = ('id', 'first_name', 'email', 'last_name', 'birth_date', 'gender', \
                  'username')
        extra_kwargs = {
                'id': { 'read_only': True},
                'username': { 'read_only': True},
                }

    def create(self, validated_data):
        print(validated_data)
        obj = DailyUser.objects.create(**validated_data)
        return obj

class TaskGetSerializer(TaskCreateSerializer):
    time_created = serializers.DateTimeField(read_only=True)
    has_finished = serializers.BooleanField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    daily_user = UserSerializer(read_only=True)


    def create(self, validated_data):
        pass

    def validate(self, attrs):
        return attrs

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTask
        fields = ('id', 'title', 'due_to')



class UserGetTaskSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()
    finished_tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = DailyUser
        fields = ('id', 'tasks', 'finished_tasks') + UserSerializer.Meta.fields

    def get_tasks(self, obj: DailyUser):
        all_tasks = obj.task.all()
        all_tasks = TaskSerializer(all_tasks, many=True)
        return all_tasks.data

    def get_finished_tasks(self, obj: DailyUser):
        all_tasks = obj.task.filter(due_to__lte=timezone.now())
        all_taks = TaskSerializer(all_tasks, many=True)
        return all_taks.data
