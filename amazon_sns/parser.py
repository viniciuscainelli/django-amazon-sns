# coding: utf-8
import json
import requests
from base64 import b64decode
from urlparse import urlparse
from M2Crypto import X509


class SNS(object):

    def __init__(self, notification, topic_arn=None):
        if isinstance(notification, (str, unicode)):
            notification = json.loads(notification)

        self.notification = notification
        self.topic_arn = topic_arn

    def is_valid(self):
        cert_url = self.notification.get('SigningCertURL')
        topic_arn = self.notification.get('TopicArn')
        type = self.notification.get('Type')

        if not cert_url or not topic_arn:
            return False

        if self.topic_arn and self.topic_arn != topic_arn:
            return False

        parsed = urlparse(cert_url)

        if not parsed.hostname.endswith('.amazonaws.com'):
            return False

        if type in ['Notification']:
            params_to_verify = ['Message', 'MessageId', 'Subject', 'Timestamp', 'TopicArn', 'Type']
        elif type in ['SubscriptionConfirmation', 'UnsubscribeConfirmation']:
            params_to_verify = ['Message', 'MessageId', 'SubscribeURL', 'Timestamp', 'Token', 'TopicArn', 'Type']
        else:
            return False

        response = requests.get(cert_url)
        if response.status_code != requests.codes.ok:
            return False

        string_to_verify = u''
        for param in params_to_verify:
            if param in self.notification and self.notification.get(param):
                string_to_verify += u'{}\n{}\n'.format(param, self.notification.get(param))

        cert = X509.load_cert_string(response.content)
        pubkey = cert.get_pubkey()
        pubkey.reset_context(md='sha1')
        pubkey.verify_init()
        pubkey.verify_update(string_to_verify.encode('utf-8'))
        result = pubkey.verify_final(b64decode(self.notification.get('Signature')))

        if result != 1:
            return False
        else:
            return True

    def is_subscription(self):
        if self.notification.get('Type') in ['SubscriptionConfirmation'] and 'SubscribeURL' in self.notification:
            return True
        return False

    def is_notification(self):
        if self.notification.get('Type') in ['Notification']:
            return True
        return False

    def subscribe(self):
        if self.is_subscription():
            response = requests.get(self.notification.get('SubscribeURL'))
            if response.status_code == requests.codes.ok:
                return True
        return False

    def get_topic_arn(self):
        return self.notification.get('TopicArn')

    def get_notification(self):
        return self.notification

    def get_message(self):
        return self.notification.get('Message')
