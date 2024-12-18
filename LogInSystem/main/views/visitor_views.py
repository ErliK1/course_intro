from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from django.http import Http404

from main.constants import DETAIL, MESSAGE
from main.utilities import create_response_data
from main.serializers.visitor_serializers import RegisterVisitorSerializer, VisitorSerializer
from main.models import Visitor
from main.permissions import VisitorPermission, ManagerPermission 


class RegisterVisitorAPIView(APIView):
    serializer_class = RegisterVisitorSerializer

    def get_serializer_class(self, ):
        return self.serializer_class

    def get_serializer(self, obj=None, data=None, many=False):
        print("Inside get_serializer")
        if obj:
            return self.get_serializer_class()(obj, many=many)
        return self.get_serializer_class()(data=data, many=many)

   
    @transaction.atomic
    def post(self, request: Request, *args, **kwargs) -> Response:
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(create_response_data(MESSAGE, "Created successfully"),
                        status=status.HTTP_200_OK)

class VisitorListAPIView(ListAPIView):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [ManagerPermission,]

    def get_queryset(self, ):
        filter_kwargs = {
                'user__first_name__icontains': self.request.query_params.get('first_name', ''),
                'user__last_name__icontains': self.request.query_params.get('last_name', ''),
                'user__username__icontains': self.request.query_params.get('username', ''),
                'user__email__icontains': self.request.query_params.get('email', ''),
        }
        query_set = Visitor.objects.filter(**filter_kwargs)
        return query_set


class VisitorRetrieveAPIView(RetrieveAPIView):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [VisitorPermission]

    def get_object(self, ):
        if Visitor.objects.filter(user=self.request.user).exists():
            return self.request.user.visitor
        query_set = Visitor.objects.filter(pk=self.kwargs.get('pk'))
        if query_set.exists():
            return query_set.first()
        raise Http404("Not Found")


