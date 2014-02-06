# coding: utf-8
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from parser import SNS
from signals import sns_notification


SNS_TOPIC_ARN = getattr(settings, 'SNS_TOPIC_ARN', None)


class SNSNotificationView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SNSNotificationView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            sns = SNS(request.body, SNS_TOPIC_ARN)
        except ValueError:
            return HttpResponseBadRequest()

        if not sns.is_valid():
            return HttpResponseBadRequest()

        if sns.is_subscription():
            if not sns.subscribe():
                return HttpResponse('subscribe not ok :(')
            else:
                return HttpResponse('subscribe ok :)')

        if sns.is_notification():

            sns_notification.send(sender=sns.get_topic_arn(), notification=sns.get_notification())

        return HttpResponse('ok :)')
