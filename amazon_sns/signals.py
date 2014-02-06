# coding: utf-8
from django.dispatch import Signal


sns_notification = Signal(providing_args=['notification'])
