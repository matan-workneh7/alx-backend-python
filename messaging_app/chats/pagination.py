from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        
        return Response({
            "count": self.page.paginator.count,      # total messages
            "next": self.get_next_link(),            # link to next page
            "previous": self.get_previous_link(),    # link to previous page
            "results": data                          # actual message data
        })
