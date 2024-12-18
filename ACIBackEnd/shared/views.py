import abc
import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render

from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework import serializers, status
from rest_framework.response import Response

from shared.constants import DATA, ERRORS, SERIALIZER_ERROR_MESSAGE
from shared.models import ACIAdmin, ACIModel
from shared.permissions import ACISuperUserPermission
from shared.serializers import CreateUserSerializer
from shared.utils import get_error_message
from shared.paginators import ACIPaginator

from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.db import transaction


# Create your views here.



class ACIListAPIView(ListAPIView, abc.ABC):
    filter_serializer_class = None
    filter_map = {}
    order_params = None
    model_class: ACIModel = None
    pagination_class = ACIPaginator
    sort_map = {}
    # ToDo - Add Paginator
    # ToDo - Perpiqu ta pergatisesh per list serializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = self.order_queryset(queryset)
        if self.paginator is not None and queryset is not None:
            queryset = self.paginator.paginate_queryset(queryset=queryset, request=request, view=self)
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def filter_queryset(self, query_set):
        query_params_for_filter = self.request.query_params.get('filter')
        exact = False
        if not query_params_for_filter:
            query_params_for_filter = self.request.query_params.get('exact')
            exact = True
        if query_params_for_filter:
            data_parsed_to_json = json.loads(query_params_for_filter)
            serializer = self.get_filter_serializer(data=json.loads(query_params_for_filter))
            query_set = self.get_queryset().filter(self.find_filter_kwargs(serializer, exact))
            if (query_set):
                query_set.distinct()
            return query_set
        query_set = self.get_queryset()
        print(query_set)
        if query_set:
            query_set.distinct()
        return query_set

    def find_filter_kwargs(self, serializer: serializers.Serializer, exact):
        dictionary_filter_kwargs = {self.find_lookup_key(serializer, k, exact): v for k, v in serializer.data.items() if v or v is False}
        return Q(**dictionary_filter_kwargs)

    def find_lookup_key(self, serializer: serializers.Serializer, key, exact):
        if not exact and isinstance(serializer.fields.get(key), serializers.CharField):
            return '{}__icontains'.format(self.filter_map.get(key))
        if not exact and isinstance(serializer.fields.get(key), serializers.ListField):
            return '{}__in'.format(self.filter_map.get(key))
        return self.filter_map.get(key)

    def get_filter_serializer_class(self):
        return self.filter_serializer_class

    def get_filter_serializer(self, data):
        try:
            serializer = self.get_filter_serializer_class()(data=data)
            serializer.is_valid(raise_exception=True)
            return serializer
        except Exception as e:
            raise ValidationError(str(e))

    def order_queryset(self, query_set):
        sort_by = self.request.query_params.get('sort')
        order_by = self.request.query_params.get('order')
        if sort_by and order_by:
            sort_by = json.loads(sort_by) 
            sort_by = sort_by.get('values')
            if order_by == 'asc':
               return query_set.order_by(*[self.sort_map.get(element) for element in sort_by])
            else:
                return query_set.order_by(
                    *list(map(lambda x: '-' + str(x), [self.sort_map.get(element) for element in sort_by])))
        return query_set

    @property 
    def paginator(self, ):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator


class ACICreateAPIView(CreateAPIView, abc.ABC):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        response_data = {}
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_headers = None
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            header = self.get_success_headers(serializer.data)
            response_data = {DATA: serializer.data}
            response_status = status.HTTP_201_CREATED
            response_headers = header
        except ValidationError as ve:
            response_data = {ERRORS: ve.get_full_details()}
            response_status = status.HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist as odne:
            response_data = {ERRORS: 'Object does not exists: {}'.format(str(odne))}
        except IntegrityError as ie:
            response_data = {ERRORS: 'Duplicated values'}
        except Exception as e:
            response_data = {ERRORS: str(e)}
        finally:
            return Response(response_data, status=response_status, headers=response_headers)


class ACIListCreateAPIView(ACICreateAPIView, ACIListAPIView):
    read_serializer_class = None
    write_serializer_class = None
    serializer_error_message = SERIALIZER_ERROR_MESSAGE

    def get_serializer_class(self):
        if self.request.method == 'GET':
            assert self.read_serializer_class or self.serializer_class, get_error_message(self.serializer_error_message, self.__class__.__name__)
            return self.read_serializer_class if self.read_serializer_class else self.serializer_class
        if self.request.method == 'POST':
            assert self.write_serializer_class or self.serializer_class, get_error_message(self.serializer_error_message, self.__class__.__name__)
            return self.write_serializer_class if self.write_serializer_class else self.serializer_class
        assert self.serializer_class, get_error_message(self.serializer_error_message, self.__class__.__name__)
        return self.serializer_class


class ACIRetrieveAPIView(RetrieveAPIView, abc.ABC):
    serializer_class = None
    read_serializer_class = None
    serializer_error_message = SERIALIZER_ERROR_MESSAGE

    def get_serializer_class(self):
        assert self.serializer_class or self.read_serializer_class, get_error_message(self.serializer_error_message, self.__class__.__name__)
        return self.serializer_class if self.serializer_class else self.read_serializer_class




class CreateACiAdminAPIView(ACICreateAPIView):
    permission_classes = [IsAuthenticated, ACISuperUserPermission]
    serializer_class = CreateUserSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        admin = ACIAdmin.objects.create(user=user)
        return Response({DATA: "Admin created successfully!"}, status=status.HTTP_201_CREATED)
        





