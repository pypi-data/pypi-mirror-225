# -*- coding:utf-8 -*-
from __future__ import unicode_literals 
from xyz_restful.mixins import BatchActionMixin
from xyz_util.statutils import do_rest_stat_action

from . import models, serializers 
from rest_framework import viewsets, decorators
from rest_framework.response import Response
from xyz_restful.decorators import register 

__author__ = 'denishuang'


@register()
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'name': ['exact'],
        'is_active': ['exact'],
        'create_time': ['range']
    }
    search_fields = ('name', 'number')
    ordering_fields = ('name',)


@register()
class BrandViewSet(viewsets.ModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'name': ['exact'],
        'is_active': ['exact'],
        'create_time': ['range']
    }
    search_fields = ('name', 'abbr')
    ordering_fields = ('name', )


@register()
class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'name': ['exact'],
        'category': ['exact'],
        'brand': ['exact'],
        'is_active': ['exact'],
        'create_time': ['range']
    }
    search_fields = ('name', 'number')
    ordering_fields = ('name', 'number')
