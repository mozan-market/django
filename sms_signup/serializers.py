# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _
from rest_framework import serializers
from .models import ActivationSMSCode

PHONE_REGEX = r'^[\d]{11,14}$'

PHONE_MAX_LENGTH = 14
ACTIVATION_CODE_MAX_LENGTH = 30

PHONE_LABEL = _(u"Номер телефона в международном формате")
PHONE_ERROR = _(u"Укажите номер телефона в международном формате (только цифры)")
USER_ALREADY_EXISTS = _(u"Пользователь с таким телефоном уже зарегистрирован")
WRONG_ACTIVATION_CODE = _(u"Неверный код активации")
WRONG_PASSWORD = _(u"Неверный пароль")
INACTIVE_ACCOUNT = _(u"Ваш аккаунт неактивен")
ACTIVATION_CODE_LABEL = _(u"Код подтверждения регистрации")
PASSOWRD_LABEL = _(u"Пароль")


class SMSSerializer(serializers.Serializer):
	phone=serializers