from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from django.db.models import Case, When
from collections import OrderedDict


from .search_filter import RefinerSearchFilter


class AdvancedInputSerializer(serializers.Serializer):
    """ Required body data for filtered list """
    filter = serializers.JSONField(default={})
    cachedIds = serializers.ListField(child=serializers.IntegerField())
    include = serializers.ListField(child=serializers.IntegerField())


class PageRequestSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.IntegerField()
    num_pages = serializers.IntegerField()
    page = serializers.IntegerField()
    limit = serializers.IntegerField()


class ResponseListSerializer(serializers.Serializer):
    listIds = serializers.ListField(child=serializers.IntegerField())
    list = serializers.ListField(child=serializers.JSONField(default={}))
    page_request = PageRequestSerializer(many=False)


class APIDataCachePagination(PageNumberPagination):
    """
        Paginate a queryset if required, either returning a
        ResponseListSerializer object, or `None` if pagination is not configured for this view.

        The pagination for api-data-cahce advanced list action is taking into
        account by removiing the cached items from each page, while preserving 
        the order of the `listIds`.

    """
    page_size = 100
    page_size_query_param = 'limit'
    max_page_size = 1000
    action = ''

    def paginate_queryset(self, queryset, request, view=None):
        self.action = view.action
        ids_to_exclude = getattr(request, 'cachedIds', None)
        order_by = request.query_params.get('orderBy', 'id').split(',')
        self.page_size = request.query_params.get(self.page_size_query_param, 100)
        main_ordering_field = order_by[0]

        if not main_ordering_field:
            order_by = ['id']

        ordered_qs = queryset.order_by(*order_by)
        if 'advanced_list' in self.action:
            list_ids_page = super().paginate_queryset(ordered_qs.values_list('pk', flat=True), request, view)
            if len(list_ids_page):
                preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(list_ids_page)])
                query_page = queryset.filter(id__in=list_ids_page).exclude(id__in=ids_to_exclude).order_by(preserved)
            else:
                query_page = []
        else:
            query_page = super().paginate_queryset(ordered_qs, request, view)
            list_ids_page = [e.id for e in query_page]

        page = [{'listIds': list_ids_page, 'list': query_page}]
        return page


    def get_paginated_response(self, data):
        _data = data

        if self.request:
            page_number = self.request.query_params.get(self.page_query_param, 1)
        else:
            page_number = None

        return Response(OrderedDict([
            ('page_request',
                 {'count': self.page.paginator.count,
                  'next': self.get_next_link(),
                   'previous': self.get_previous_link(),
                   'num_pages': self.page.paginator.num_pages,
                   'page': page_number,
                   'limit': self.page_size,
                 }
             ),
            ('list', _data['list']),
            ('listIds', _data['listIds'])
        ]))





class APIDataCacheListViewMixin(object):
    """List objects."""
    pagination_class = APIDataCachePagination
    filter_backends = [RefinerSearchFilter]
    include_in_search_results = []
    search_custom_property_entity = None

    def __init__(self, *initargs, **initkwargs):
        self.include_in_search_results = []
        return super().__init__(*initargs, **initkwargs)

    @staticmethod
    def _convert_to_django_filter_syntax(filter_params):
        django_filter = {}
        django_exclude = {}

        for javascript_field in filter_params.keys():
            field = javascript_field.replace(".", '__')
            if field.startswith("!"):
                django_exclude[field[1:]] = filter_params[javascript_field]
            else:
                django_filter[field] = filter_params[javascript_field]
        return django_filter, django_exclude



    def get_filtered_query(self, request, queryset=None):
        diff = request.data.get('cachedIds', [])
        include_ids = request.data.get('include', [])
        filter_params = request.data.get('filter', {})
        request.cachedIds = diff
        
        self.include_in_search_results = include_ids
        if queryset is None:
            queryset = self.get_queryset()
        if bool(filter_params):
            django_filter, django_exclude = self._convert_to_django_filter_syntax(filter_params)
            queryset = queryset.filter(**django_filter).exclude(**django_exclude)

        return queryset


    @action(methods=['POST'], detail=False, url_path= settings.ADVANCED_LIST_ENDPOINT, url_name='advanced_list')
    def advanced_list(self, request, queryset=None, *args, **kwargs):
        """ List operation with filtered results.

            `filter` works as SQL WHERE clause to filter results. It follows the Django filter notation.

            `cachedIds` is used  to exclude instances from the output, `body.list`.

            `include` is used to force the sorted inclusion of the object ids in the output `body.listIds`, it cannot override the filter exclusion.

        """
        self.queryset = self.get_filtered_query(request, queryset)
        return self.list(request, self.queryset, *args, **kwargs)

    def list(self, request, queryset=None, *args, **kwargs):
        if queryset is None:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            list = page[0]['list']
            listIds = page[0]['listIds']

            serializer = self.get_serializer(list, many=True)
            serialized_data = {'list': serializer.data, 'listIds': listIds}
            return self.get_paginated_response(serialized_data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
