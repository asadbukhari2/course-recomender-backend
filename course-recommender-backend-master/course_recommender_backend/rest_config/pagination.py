from rest_framework import pagination


class RESTAPIPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 10


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20
