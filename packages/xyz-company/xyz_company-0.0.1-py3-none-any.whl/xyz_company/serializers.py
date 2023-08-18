# -*- coding:utf-8 -*-
# author : 'denishuang'
from xyz_restful.mixins import IDAndStrFieldSerializerMixin
from rest_framework import serializers
from . import models
import logging

log = logging.getLogger("django")


class CompanySerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Company
        exclude = ()
