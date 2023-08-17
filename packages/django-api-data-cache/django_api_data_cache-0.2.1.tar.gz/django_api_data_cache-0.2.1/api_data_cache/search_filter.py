from rest_framework import filters
import re



class RefinerSearchFilter(filters.SearchFilter):
    search_field_dict = {}
    custom_property_entity = None

    def filter_queryset(self, request, queryset, view):
        #  1 - search in regular fields that were pre-defined in the view()
        qs_regular_search = super().filter_queryset(request, queryset, view)

        self.custom_property_entity = view.search_custom_property_entity
        search_results_ids = []

        try:
            included_by_requester = queryset.filter(id__in=view.include_in_search_results)
        except:
            included_by_requester = queryset.none()

        # 1 + 2 + 3
        queryset = qs_regular_search | \
                   queryset.filter(id__in=search_results_ids) | \
                   included_by_requester

        return queryset.distinct()

    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params, search_field_dict = strip_search_fields(request.query_params.get(self.search_param, ''))
        self.search_field_dict = search_field_dict
        return params.replace(',', ' ').split()




def strip_search_fields(qsearch):
    if not qsearch:
        return '', {}
    search_text = re.sub(':', ' ', re.sub('\{([^\{]*)\}', ' ', qsearch))
    search_field = {}
    sub_string_brackets = re.search('\{([^\{]*)\}', qsearch)
    if sub_string_brackets:
        segments = sub_string_brackets.group().split(':')
        for idx in range(0, len(segments), 1):
            value = ''
            label = segments[idx]
            between_quotes = re.findall('"([^"]*)"', label)
            if between_quotes: label = between_quotes[-1]
            if idx < (len(segments) - 1):
                value = segments[idx + 1]
                between_quotes = re.findall('"([^"]*)"', value)
                if between_quotes: value = between_quotes[0]

            if value:
                search_field[label] = value

    return search_text, search_field