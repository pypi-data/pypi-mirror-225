#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:denishuang

from __future__ import unicode_literals

from django.apps import AppConfig


class Config(AppConfig):
    name = 'xyz_company'
    label = 'company'
    verbose_name = '公司'

    def ready(self):
        super(Config, self).ready()
        # from . import receivers