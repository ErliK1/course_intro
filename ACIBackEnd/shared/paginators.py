from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response

from collections import OrderedDict

class ACIPaginator(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 4
    
    def get_paginated_response(self, data):
        return Response(OrderedDict({
            'data': data,
            'pagination': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            }
        }))
