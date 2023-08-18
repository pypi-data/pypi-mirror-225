# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Category(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "目录"
        ordering = ('-is_active', '-create_time')

    name = models.CharField("名字", max_length=128, unique=True)
    abbr = models.CharField("缩写", max_length=32, blank=True, default='')
    is_active = models.BooleanField("有效", default=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.abbr or self.name


class Brand(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "品牌"
        ordering = ('-is_active', '-create_time')

    name = models.CharField("名字", max_length=128, unique=True)
    abbr = models.CharField("缩写", max_length=32, blank=True, default='')
    is_active = models.BooleanField("有效", default=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.abbr or self.name


class Product(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "产品"
        ordering = ('-is_active', '-create_time')

    name = models.CharField("名字", max_length=128, unique=True)
    number = models.CharField("编号", max_length=32, blank=True, default='')
    abbr = models.CharField("缩写", max_length=32, blank=True, default='')
    category = models.ForeignKey(Category, verbose_name=Category._meta.verbose_name,
                                 null=True, blank=True, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, verbose_name=Brand._meta.verbose_name,
                              null=True, blank=True, on_delete=models.PROTECT)
    is_active = models.BooleanField("有效", default=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.abbr or self.name
