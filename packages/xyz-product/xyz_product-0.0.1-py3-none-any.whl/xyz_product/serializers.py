# -*- coding:utf-8 -*-
# author : 'denishuang'
from xyz_restful.mixins import IDAndStrFieldSerializerMixin
from rest_framework import serializers
from . import models
import logging

log = logging.getLogger("django")


class BrandSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        exclude = ()


class CategorySerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Category
        exclude = ()


class ProductSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Product
        exclude = ()
