import decimal
import json
import sys
import time
from datetime import timedelta
from pathlib import Path
from decimal import Decimal
import math
import random
from uuid import uuid4

from django.core.cache import cache
from django.db.models import Q
from django.forms import model_to_dict
from django.utils import timezone
from django.utils.datetime_safe import datetime
import pytz
from numpy.core.defchararray import upper
from main.settings import BASE_DIR
from .finance_transact_service import FinanceTransactService
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
import os


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, int):
                return int(obj)
            elif isinstance(obj, float) or isinstance(obj, decimal.Decimal):
                return float(obj)
            if isinstance(obj, datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(obj, datetime.date):
                return obj.strftime('%Y-%m-%d')
            if isinstance(obj, time) or isinstance(obj, timedelta):
                return obj.__str__()
            else:
                return json.JSONEncoder.default(self, obj)
        except Exception as e:
            # logger.exception(e, stack_info=True)
            return obj.__str__()


class FinanceLaborService:

    # 资金数据写入服务
    @staticmethod
    def larbor_add(params):
        data = []
        order_no = params.get('order_no', "")  # 订单号
        account_id = params.get("account_id", "")  # 账户
        their_account_id = params.get("their_account_id", "")  # 对方账户
        their_account_bank_card_id = params.get("their_account_bank_card_id", "")  # 入账银行
        transact_time = params.get("transact_time", "")  # 汇入时间
        amount = params.get("amount", "")  # 汇入金额
        remark = params.get("remark", "")  # 扣款依据（备注）
        manage_point = params.get("manage_point", "")  # 管理费点数
        management_fees = params.get("management_fees", "")  # 管理费金额
        tax_point = params.get("tax_point", "")  # 税金点数
        taxes = params.get("taxes", "")  # 税金
        brokerage_point = params.get("brokerage_point", "")  # 佣金点数
        commission = params.get("commission", "")  # 佣金
        # amount_remitted = params.get("amount_remitted", "")  # 汇出金额
        # remit_time = params.get("remit_time", "")  # 汇出时间
        images = params.get("images", "")  # 凭证照片
        collection = params.get("collection", "")  # 收款列表
        info_data = {
            'account_id': account_id,
            'their_account_id': their_account_id,
            'order_no': order_no,
            'relate_uuid': uuid4()
        }

        # 汇入数据
        import_data = info_data.copy()
        import_data['transact_time'] = transact_time
        import_data['amount'] = abs(Decimal(amount))
        import_data['remark'] = remark
        data.append(import_data)

        if manage_point:
            # 管理费数据
            manage_data = info_data.copy()
            manage_data['manage_point'] = manage_point
            manage_data['amount'] = -abs(Decimal(management_fees))
            manage_data['sand_box'] = "MANAGEMENT_FEE_RECEIVABLE"
            data.append(manage_data)
        if tax_point:
            # 税金数据
            taxes_data = info_data.copy()
            taxes_data['tax_point'] = tax_point
            taxes_data['amount'] = -abs(Decimal(taxes))
            taxes_data['sand_box'] = "TAX_RECEIVABLES"
            data.append(taxes_data)
        if brokerage_point:
            # 佣金数据
            commission_data = info_data.copy()
            commission_data['tax_point'] = brokerage_point
            commission_data['amount'] = -abs(Decimal(commission))
            commission_data['sand_box'] = "COMMISSION_RECEIVABLE"
            data.append(commission_data)
        # if amount_remitted:
        #     # 汇出数据
        #     remit_data = info_data.copy()
        #     remit_data['brokerage_point'] = brokerage_point
        #     remit_data['transact_time'] = remit_time
        #     remit_data['amount'] = -abs(Decimal(amount_remitted))
        #     data.append(remit_data)

        if collection:
            # 汇出数据
            for i in collection:
                remit_data = info_data.copy()
                remit_data['their_account_bank_card_id'] = i['their_account_bank_card_id']
                remit_data['their_account_id'] = i['their_account_id']
                remit_data['amount'] = -abs(Decimal(i['amount_remitted']))
                data.append(remit_data)

        # try:
        #     for item in data:
        #         thread, thread_err = FinanceTransactService.add(item)
        #         if thread_err:
        #             return None, thread_err
        # except Exception as e:
        #     return None, str(e)

        print(data)
        return None, None
