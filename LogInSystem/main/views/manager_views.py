from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from main.models import Manager
from main.serializers.manager_serializers import ManagerRegisterSerializer
from main.permissions import ManagerPermission
from main.utilities import create_response_data
from main.constants import DETAIL



class ManagerRegisterAPIView(CreateAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerRegisterSerializer
    permission_classes = [IsAuthenticated, ManagerPermission]

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
       serializer = self.get_serializer(data=request.data) 
       serializer.is_valid(raise_exception=True)
       serializer.save()
       return Response(create_response_data(DETAIL, "Manager created successfully"), 
                       status=status.HTTP_201_CREATED)

class ManagerRetrieveAPIView(RetrieveAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerRegisterSerializer
    permission_classes = [ManagerPermission]


    def get_object(self, ):
        return Manager.objects.get(user=self.request.user)





