from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'has_next': self.page.has_next(),
            'total_pages': self.page.paginator.num_pages,
            'results': data,
        })
        # return super().get_paginated_response(data)