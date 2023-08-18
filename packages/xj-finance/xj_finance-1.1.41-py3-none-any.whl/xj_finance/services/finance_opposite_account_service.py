import time
import os
import datetime

from django.db.models import Q
from django.db.models import F
from rest_framework.response import Response

from ..models import OppositeAccount


class FinanceOppositeAccountService:

    @staticmethod
    def get():
        currencies = OppositeAccount.objects.all().annotate(value=F('opposite_account'))

        return list(currencies.values('id', 'value', 'opposite_account_code'))

    @staticmethod
    def post(params):
        opposite_account_code = params.get('opposite_account_code', '')
        opposite_account = params.get('value', '')
        if opposite_account_code:
            opposite_account_code_set = OppositeAccount.objects.filter(
                opposite_account_code=opposite_account_code).first()
            if opposite_account_code_set is not None:
                return None, "opposite_account_code已存在"
        try:
            OppositeAccount.objects.create(**params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)

    @staticmethod
    def put(params):
        pay = {}
        id = params.get('id', '')
        opposite_account_code = params.get('opposite_account_code', '')
        if opposite_account_code:
            pay['opposite_account_code'] = opposite_account_code
        if opposite_account_code:
            pay['opposite_account'] = params.get('value', '')
        opposite_account_code_set = OppositeAccount.objects.filter(id=id).first()
        if opposite_account_code_set is None:
            return None, "数据不存在"
        try:
            OppositeAccount.objects.filter(id=id).update(**pay)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)

    @staticmethod
    def list():
        currencies = OppositeAccount.objects.all().annotate(value=F('opposite_account'))

        return list(currencies.values('id', 'value', 'opposite_account_code')), None

    @staticmethod
    def add(params):
        opposite_account_code = params.get('opposite_account_code', '')
        opposite_account = params.get('opposite_account', '')
        if opposite_account_code:
            opposite_account_code_set = OppositeAccount.objects.filter(
                opposite_account_code=opposite_account_code).first()
            if opposite_account_code_set is not None:
                return None, "opposite_account_code已存在"
        try:
            OppositeAccount.objects.create(**params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)

    @staticmethod
    def edit(params):
        pay = {}
        id = params.get('id', '')
        opposite_account_code = params.get('opposite_account_code', '')
        opposite_account = params.get('opposite_account', '')
        if opposite_account_code:
            pay['opposite_account_code'] = opposite_account_code
        if opposite_account:
            pay['opposite_account'] = opposite_account
        opposite_account_code_set = OppositeAccount.objects.filter(id=id).first()
        if opposite_account_code_set is None:
            return None, "数据不存在"
        try:
            OppositeAccount.objects.filter(id=id).update(**pay)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)
