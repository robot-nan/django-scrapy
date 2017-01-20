#coding:utf-8
from django.conf import settings
from mongoengine import *

connect(settings.MONGO_DATABASE, host=settings.MONGO_HOST, port=settings.MONGO_PORT, username=settings.MONGO_USERNAME,
        password=settings.MONGO_PASSWORD)

