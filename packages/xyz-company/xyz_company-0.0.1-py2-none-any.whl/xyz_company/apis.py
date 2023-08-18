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
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'name': ['exact'],
        'number': ['exact']
    }
    search_fields = ('name', 'number')
    ordering_fields = ('name', 'number')
