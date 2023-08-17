=======================================
Django API Data Cache
=======================================

API Data Cache is a simple mixin for Django REST framework to serve database
objects to clients using the api_data_cache service.

It is composed of a mixing for list views that processes the request parameters from api_data_cache 
clients for pagination and filtering.


Installation
------------

1. Install the package using pip:

   .. code-block:: bash

       pip install django_api_data_cache


2. Add `'api_data_cache'` to your Django project's `INSTALLED_APPS` list in the `settings.py` file:

   .. code-block:: python

       INSTALLED_APPS = [
           # ...
           'rest_framework',
           'api_data_cache',
           # ...
       ]



Usage
-----

1. Import the `APIDataCacheListViewMixin` into your view module:

   .. code-block:: python

       from api_data_cache.mixins import APIDataCacheListViewMixin

2. Inherit the `APIDataCacheListViewMixin` in your view class:

   .. code-block:: python

       from api_data_cache.mixins import APIDataCacheListViewMixin
       from rest_framework import viewsets
       from .models import YourModel
       from .serializer import YourPartialSerializer


       class YourListView(APIDataCacheListViewMixin, viewsets.GenericViewSet):
           queryset = YourModel.objects.all()
           serializer_class = YourPartialSerializer
           search_fields = ['field1', 'field2']


