# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Company(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "公司"
        ordering = ('-is_active', '-create_time')

    name = models.CharField("名字", max_length=128, unique=True)
    number = models.CharField("编号", max_length=32, unique=True)
    abbr = models.CharField("缩写", max_length=32, blank=True, default='')
    is_active = models.BooleanField("有效", default=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.abbr or self.name
