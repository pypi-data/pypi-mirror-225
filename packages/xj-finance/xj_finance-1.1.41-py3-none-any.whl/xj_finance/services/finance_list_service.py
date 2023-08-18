from decimal import Decimal
# from elasticsearch import Elasticsearch
import json
from logging import getLogger
from pathlib import Path
import sys
from datetime import datetime
from django.db.models import Sum, F, Q
from django.db.models import Max, OuterRef, Subquery
from django.forms import model_to_dict
import pytz
from numpy.core.defchararray import upper
from rest_framework import serializers
from django.db import transaction
from main.settings import BASE_DIR
from xj_enroll.utils.custom_tool import format_params_handle
from xj_finance.services.finance_extend_service import FianceExtendService
from xj_finance.services.finance_transact_service import FinanceTransactService
from xj_finance.utils.custom_tool import filter_result_field, write_to_log, force_transform_type, dynamic_load_class, \
    format_list_handle, filter_fields_handler
from xj_thread.services.thread_list_service import ThreadListService
from xj_thread.utils.join_list import JoinList
from xj_user.models import BaseInfo, Platform
from xj_user.services.user_bank_service import UserBankCardsService
from xj_user.services.user_detail_info_service import DetailInfoService
from xj_user.services.user_platform_service import UserPlatformService
from xj_user.services.user_service import UserService
from .finance_service import FinanceService
from ..models import Transact, PayMode, FinanceMainExtendField
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.utility_method import keep_two_decimal_places, get_current_time, format_dates

logger = getLogger('log')

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_finance"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_finance"))

sand_box_meet = main_config_dict.sand_box_meet or module_config_dict.sand_box_meet or ""
sand_box_receivable = main_config_dict.sand_box_receivable or module_config_dict.sand_box_receivable or ""
sand_box_cash_withdrawal = main_config_dict.sand_box_cash_withdrawal or module_config_dict.sand_box_cash_withdrawal or ""


class FinanceListService:
    finance_detail_expect_extend = [i.name for i in Transact._meta.fields if not "field_" in i.name]
    finance_detail_remove_fields = [i.name for i in Transact._meta.fields if "field_" in i.name]

    finance_base_fields = [i.name for i in Transact._meta.fields]
    # 用户详情表字段
    finance_detail_fields = [i.name for i in Transact._meta.fields] + ["finance_id"]
    finance_detail_expect_extend = [i.name for i in Transact._meta.fields if not "field_" in i.name] + ["finance_id"]
    finance_detail_remove_fields = [i.name for i in Transact._meta.fields if "field_" in i.name] + ["id", "finance"]
    # 详情信息扩展字段获取
    field_map_list = list(FinanceMainExtendField.objects.all().values("field", 'field_index'))

    @staticmethod
    def list(params, user_id, filter_fields: "str|list" = None):

        # ========== 相关前置业务逻辑处理 start ==========
        res_list = []
        page = int(params['page']) - 1 if 'page' in params else 0
        size = int(params['size']) if 'size' in params else 10
        print(params)
        valid = FinanceService.check_filter_validity(params=params)
        if valid['err'] > 0:
            return None, valid['msg']
        if params.get("is_all", None):
            transacts = Transact.objects.filter(**valid['query_dict'])
        else:
            transacts = Transact.objects.filter(account_id=user_id).filter(**valid['query_dict'])

        if params.get("is_enroll", None):
            transacts = Transact.objects.filter(enroll_id__isnull=False).filter(**valid['query_dict'])
        if params.get("is_thread", None):
            transacts = Transact.objects.filter(thread_id__isnull=False).filter(**valid['query_dict'])

        if not params.get("sand_box", None) and params.get("is_withdraw", None):
            transacts = transacts.filter(~Q(bookkeeping_type='WITHDRAW'))

        # 处理filter_fields，获取ORM查询字段列表
        filter_fields_list = filter_fields_handler(
            input_field_expression=filter_fields,
            all_field_list=FinanceListService.finance_base_fields
        )
        filter_fields_list = list(set(filter_fields_list + ["thread_id", "id"]))

        params = format_params_handle(
            param_dict=params,
            is_remove_empty=True,
            filter_filed_list=[
                "id|int", "id_list|list", "thread_id|int", "sand_box_id|int", "sand_box_list|list",
                "thread_id_list|list", "their_account_id_list|list", "account_id_list|list",
                "account_id|int", "their_account_id|int", "enroll_id|int", "pay_mode_id|int",
                "enroll_id_list", "enroll_record_id_list|list",
                "transact_time_start|date", "transact_time_end|date",
                "finance_status_code", "sand_box_status_code"
            ],
            split_list=["sand_box_list", "thread_id_list", "id_list", "enroll_id_list", "enroll_record_id_list",
                        "their_account_id_list", "account_id_list", ],
            alias_dict={
                "transact_time_start": "transact_time__gte", "transact_time_end": "transact_time__lte",
                "sand_box_list": "sand_box_id__in", "thread_id_list": "thread_id__in", "id_list": "id__in",
                "their_account_id_list": "their_account_id__in", "account_id_list": "account_id__in",
                "enroll_id_list": "enroll_id__in", "enroll_record_id_list": "enroll_record_id__in"
            },
        )
        transacts = transacts.extra(select={'transact_time': 'DATE_FORMAT(transact_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
                                            'create_time': 'DATE_FORMAT(create_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})

        transacts = transacts.annotate(pay_mode_code=F("pay_mode__pay_mode"),
                                       pay_mode_value=F("pay_mode__pay_value"),
                                       sand_box_name=F("sand_box__sand_box_name")
                                       )
        transacts = transacts.order_by('-create_time')
        transacts = transacts.filter(**params).values(*filter_fields_list)
        # ========== 相关前置业务逻辑处理 end ==========

        # ========== 翻页 start ==========
        total = transacts.count()
        income = transacts.aggregate(income=Sum("income"))
        outgo = transacts.aggregate(outgo=Sum("outgo"))
        current_page_set = transacts[page * size: page * size + size] if page >= 0 and size > 0 else transacts
        # ========== 翻页 end ==========

        for i, it in enumerate(current_page_set):
            it['order'] = page * size + i + 1
            it['balance'] = keep_two_decimal_places(it['balance'])
            it['amount'] = keep_two_decimal_places(it['income']) if it[
                                                                        'income'] > 0 else keep_two_decimal_places(
                -abs(float(it['outgo'])))
            it['income'] = keep_two_decimal_places(it['income'])
            it['outgo'] = keep_two_decimal_places(it['outgo'])
            res_list.append(it)

        data = res_list
        # ================== 对方账户适配（xj_user）start ===============================
        their_user_id_list = [item.get("their_account_id", None) for item in res_list]
        their_user_list, err = DetailInfoService.get_list_detail(user_id_list=their_user_id_list)
        if their_user_list:
            data = JoinList(res_list, their_user_list, "their_account_id", "user_id").join()

        data = filter_result_field(
            result_list=filter_result_field(  # 扩展字段替换
                result_list=data,
                alias_dict={"id": "finance_id", "full_name": "their_full_name", "real_name": "their_real_name",
                            "user_name": "their_account_name",
                            "nickname": "their_nickname", "phone": "their_phone"},
            ),
        )
        # ================== 对方账户适配（xj_user）end ===============================

        # ================== 账户适配（xj_user）start ===============================
        user_id_list = [item.get("account_id", None) for item in data]
        user_list, err = DetailInfoService.get_list_detail(user_id_list=user_id_list)
        if user_list:
            data = JoinList(data, user_list, "account_id", "user_id").join()

        data = filter_result_field(
            result_list=filter_result_field(  # 扩展字段替换
                result_list=data,
                alias_dict={"user_name": "account_name"},
            ),
        )
        # ================== 账户适配（xj_user）end ===============================

        # ================== 账户银行卡适配（xj_user）start ===============================
        account_bank_card_id_list = [item.get("account_bank_card_id", None) for item in res_list]
        account_bank_card_list, err = UserBankCardsService.get_bank_card(allow_user_list=account_bank_card_id_list)
        if account_bank_card_list:
            data = JoinList(data, account_bank_card_list['list'], "account_bank_card_id", "id").join()

        data = filter_result_field(
            result_list=filter_result_field(  # 扩展字段替换
                result_list=data,
                alias_dict={"id": "account_bank_card_id", "bank_card_num": "account_bank_card_num",
                            "open_account_bank": "account_open_account_bank", },
            ),
        )
        # ================== 账户银行卡适配（xj_user）end ===============================

        # ================== 对方账户银行卡适配（xj_user）start===============================
        their_account_bank_card_id_list = [item.get("their_account_bank_card_id", None) for item in res_list]
        their_account_bank_card_list, err = UserBankCardsService.get_bank_card(
            allow_user_list=their_account_bank_card_id_list)
        if their_account_bank_card_list:
            data = JoinList(data, their_account_bank_card_list['list'], "their_account_bank_card_id", "id").join()

        data = filter_result_field(
            result_list=filter_result_field(  # 扩展字段替换
                result_list=data,
                alias_dict={"id": "their_account_bank_card_id", "bank_card_num": "their_bank_card_num",
                            "open_account_bank": "their_open_account_bank", },
            ),
        )
        # ================== 对方账户银行卡适配（xj_user）end ===============================

        # ================== 平台适配（xj_user）start ===============================
        platform_id_list = [item.get("platform_id", None) for item in data]
        platform_list, err = UserPlatformService.list(id_list=platform_id_list)
        if platform_list:
            data = JoinList(data, platform_list['list'], "platform_id", "platform_id").join()

        data = filter_result_field(
            result_list=filter_result_field(  # 扩展字段替换
                result_list=data,
                alias_dict={"id": "platform_id"},
            ),
        )
        # ================== 平台适配（xj_user）end ===============================

        # ================== 报名信息适配（xj_enroll）start ===============================
        if not sys.modules.get("xj_enroll.service.enroll_services.EnrollServices"):
            from xj_enroll.service.enroll_services import EnrollServices

            enroll_id_list = [item.get("enroll_id", None) for item in data]
            enroll_list, err = EnrollServices.enroll_list({"id_list": enroll_id_list}, "thread_id")
            if enroll_list:
                data = JoinList(data, enroll_list['list'], "enroll_id", "id").join()
        # ================== 报名信息适配（xj_enroll）end ===============================

        # ================== 信息模块适配（xj_thread）start ===============================
        thread_id_list = [item.get("thread_id", None) for item in data]
        thread_list, err = ThreadListService.search(thread_id_list, filter_fields="title")
        if thread_list:
            data = JoinList(data, thread_list, "thread_id", "id").join()

        extend_id_list = [item.get("finance_id", None) for item in data]
        extend_list, err = FianceExtendService.get_extend_info(extend_id_list)
        if extend_list:
            data = JoinList(data, extend_list, "finance_id", "finance_id").join()
        # ================== 信息模块适配（xj_thread）end ===============================

        # ======================= section ORM查村字段过滤 start ==============================
        field_map_list = FinanceListService.field_map_list
        field_map = {item['field_index']: item['field'] for item in field_map_list}
        data = filter_result_field(
            result_list=filter_result_field(  # 扩展字段替换
                result_list=data,
                alias_dict=field_map,
            ),
            remove_filed_list=FinanceListService.finance_detail_remove_fields,  # 移除未配置的扩展字段已经主键ID
        )
        # ======================= section ORM查村字段过滤 end ==============================

        income = income.get("income", "0.0")
        outgo = outgo.get("outgo", "0.00")
        statistics = {
            "income": keep_two_decimal_places(
                income) if income else "0.00",
            "outgo": keep_two_decimal_places(
                outgo) if outgo else "0.00",
        }
        return {'size': int(size), 'page': int(page + 1), 'total': total, 'list': data,
                "statistics": statistics}, None

    @staticmethod
    def detail(pk=None, order_no=None, transact_no=None, field_list=None):
        """
        查询订单-单笔订单
        """
        if not pk and not order_no and not transact_no:
            return None, "条件不能为空"
        transact_obj = Transact.objects
        transact_obj = transact_obj.extra(
            select={'transact_time': 'DATE_FORMAT(transact_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})
        transact_obj = transact_obj.annotate(
            pay_mode_code=F("pay_mode__pay_mode"),
            pay_mode_value=F("pay_mode__pay_value"),
            sand_box_name=F("sand_box__sand_box_name")
        )
        if pk:
            transact_filter_obj = transact_obj.filter(id=pk).first()
        elif order_no:
            transact_filter_obj = transact_obj.filter(order_no=order_no).first()
        elif transact_no:
            transact_filter_obj = transact_obj.filter(transact_no=transact_no).first()
        else:
            return None, "没有找到对应的数据"

        if not transact_filter_obj:
            return None, "没有找到对应的数据"

        transact_dict = transact_filter_obj.to_json()

        transact_filter_dict = format_params_handle(
            param_dict=transact_dict,
            filter_filed_list=field_list
        )
        transact_filter_dict['amount'] = keep_two_decimal_places(
            transact_filter_dict['income']) if transact_filter_dict[
                                                   'income'] > 0 else keep_two_decimal_places(
            -abs(float(transact_filter_dict['outgo'])))
        transact_filter_dict['income'] = keep_two_decimal_places(
            transact_filter_dict['income'])
        transact_filter_dict['outgo'] = keep_two_decimal_places(
            -abs(float(transact_filter_dict['outgo'])))
        transact_filter_dict['balance'] = keep_two_decimal_places(
            float(transact_filter_dict['balance']))

        extend_id_list = [transact_filter_dict.get("id", None)]
        extend_list, err = FianceExtendService.get_extend_fields()
        if extend_list:
            transact_filter_dict.update(extend_list[0])
        return transact_filter_dict, None

    @staticmethod
    def detail_all(order_no=None, is_ledger=None):
        """
        查询订单-多笔订单
        """
        where = {}
        if not order_no:
            return None, "条件不能为空"
        where['order_no'] = order_no

        transact_obj = Transact.objects
        if not is_ledger:
            where['sand_box__isnull'] = False
        transact_filter_obj = transact_obj.filter(**where).annotate(
            sand_box_name=F("sand_box__sand_box_name")
        ).values("platform_id",
                 "transact_no",
                 "thread_id",
                 "order_no",
                 "enroll_id",
                 "enroll_record_id",
                 "account_id",
                 "their_account_id",
                 "transact_time",
                 "summary",
                 "currency_id",
                 "pay_mode_id",
                 "opposite_account_id",
                 "income",
                 "outgo",
                 "balance",
                 "goods_info",
                 "pay_info",
                 "remark",
                 "images",
                 "direction",
                 'sand_box_name',
                 "finance_status_code",
                 "bookkeeping_type",
                 "account_bank_card_id",
                 "their_account_bank_card_id",
                 'create_time',
                 "field_1", "field_2", "field_3", "field_4", "field_5",
                 "field_6",
                 "field_7", "field_8", "field_9", "field_10",
                 "field_11",
                 "field_12", "field_13", "field_14", "field_15"
                 )
        if not transact_filter_obj:
            return None, "没有找到对应的数据"
        # ======================= section ORM查村字段过滤 start ==============================
        data = list(transact_filter_obj)
        field_map_list = FinanceListService.field_map_list
        field_map = {item['field_index']: item['field'] for item in field_map_list}
        data = filter_result_field(
            result_list=filter_result_field(  # 扩展字段替换
                result_list=data,
                alias_dict=field_map,
            ),
            remove_filed_list=FinanceListService.finance_detail_remove_fields,  # 移除未配置的扩展字段已经主键ID
        )
        if is_ledger:
            for item in data:
                if item['income'] > 0:
                    item['ledger_type'] = "汇入金额"
                if item['outgo'] > 0:
                    item['ledger_type'] = "汇出金额"
                if item['sand_box_name'] == 'INVOICE_RECEIVABLE':
                    item['ledger_type'] = "开票金额"
                if item['sand_box_name'] == 'MANAGEMENT_FEE_RECEIVABLE':
                    item['ledger_type'] = "管理费金额"
                if item['sand_box_name'] == 'TAX_RECEIVABLES':
                    item['ledger_type'] = "税金金额"
                if item['sand_box_name'] == 'COMMISSION_RECEIVABLE':
                    item['ledger_type'] = "佣金金额"
                item['amount'] = keep_two_decimal_places(item['income']) if item[
                                                                                'income'] > 0 else keep_two_decimal_places(
                    -abs(float(item['outgo'])))
        # ======================= section ORM查村字段过滤 end ==============================
        return data, None

    @staticmethod
    def examine_approve(params):
        order_no = params.get("order_no", "")
        type = upper(params.get("type", "WRITE_OFF"))
        images = params.get("images", "")
        account_bank_card_id = params.get("account_bank_card_id", "")
        write_off_time = params.get("write_off_time", "")
        reverse_time = params.get("reverse_time", "")
        # 查看所有相关的订单
        finance_transact_data, err = FinanceListService.detail_all(order_no=order_no)
        if err:
            return None, err
        data = {}
        transact_list = []
        if type == "WRITE_OFF":  # 核销

            data = {
                "is_write_off": 1,
                "write_off_time": write_off_time
            }
        elif type == "REVERSE":  # 红冲
            data = {
                "is_reverse": 1,
                "reverse_time": reverse_time
            }
        elif type == "CASH_WITHDRAWAL":  # 提现
            data = {
                "is_write_off": 1,
                "sand_box_status_code": "WITHDRAW"
            }
        elif type == "TRANSFERED":  # 转账
            # 生成真实记录成功后 原沙盒记录改为核销
            data = {
                "is_write_off": 1,
                "finance_status_code": 232,
                "sand_box_status_code": "TRANSFERED",
            }
        elif type == "REFUSE":
            data = {
                "finance_status_code": 615,
                "sand_box_status_code": "TRANSFERED",
            }
        for index, friend in enumerate(finance_transact_data):
            transact_no = friend['transact_no']
            obj = Transact(
                platform_id=friend['platform_id'],
                transact_no=FinanceService.make_unicode(str(transact_no)),
                thread_id=friend['thread_id'],
                order_no=friend['order_no'],
                enroll_id=friend['enroll_id'],
                enroll_record_id=friend['enroll_record_id'],
                account_id=friend['account_id'],
                their_account_id=friend['their_account_id'],
                transact_time=get_current_time(),
                summary=friend['summary'],
                currency_id=friend['currency_id'],
                pay_mode_id=friend['pay_mode_id'],
                opposite_account_id=friend['opposite_account_id'],
                income=friend['income'],
                outgo=friend['outgo'],
                goods_info=friend['goods_info'],
                pay_info=friend['pay_info'],
                remark=friend['remark'],
                images=friend['images'],
                finance_status_code=friend['finance_status_code'],
                bookkeeping_type=friend['bookkeeping_type'],
                account_bank_card_id=friend['account_bank_card_id'],
                their_account_bank_card_id=friend['their_account_bank_card_id'],
                direction=friend['direction'],
                create_time=friend['create_time']

            )

            if not err and type == "CASH_WITHDRAWAL" and account_bank_card_id:
                if friend['account_bank_card_id'] and not friend[
                    'their_account_bank_card_id']:  # 如果account_bank_card_id不为空就是提现方
                    obj.their_account_bank_card_id = account_bank_card_id
                else:
                    obj.account_bank_card_id = account_bank_card_id
            transact_list.append(obj)
        # 转账审核成功时 报名记录进行修改
        if not err and type == "TRANSFERED":
            EnrollServices, import_err = dynamic_load_class(import_path="xj_enroll.service.enroll_services",
                                                            class_name="EnrollServices")
            assert not import_err
            pay_call_back_data, pay_call_back_err = EnrollServices.bxtx_pay_call_back(order_no)
            if pay_call_back_err:
                write_to_log(
                    prefix="转账审核成功时 报名记录进行修改",
                    content="订单号:" + str(order_no),
                    err_obj=str(pay_call_back_err)
                )
                return None, "报名修改失败"
        # 原记录核销并生成新的记
        try:
            Transact.objects.bulk_create(transact_list)  # 批量创建
            Transact.objects.filter(order_no=order_no).update(**data)  # 修改
        except Exception as e:
            write_to_log(
                prefix="原记录核销并生成新的记录",
                content="修改信息:" + str(data) + "新数据" + str(transact_list),
                err_obj=str(e)
            )
            return None, str(e)

        return None, None

    # 创建并核销
    @staticmethod
    @transaction.atomic
    def finance_create_or_write_off(data):
        data['action'] = "收入"
        sid = transaction.savepoint()
        try:
            finance_order, err_txt = FinanceTransactService.finance_flow_writing(params=data, finance_type='TRANSACT')
            if finance_order:
                params = {"order_no": finance_order['user'].get("order_no", ""), "type": "write_off"}
                finance_examine_approve, err_examine_approve = FinanceListService.examine_approve(params)
                if finance_examine_approve:
                    return None, None
                write_to_log(
                    prefix="分销 创建并核销",
                    content="数据:" + str(data),
                    err_obj=str(err_examine_approve)
                )
                return None, err_examine_approve

            write_to_log(
                prefix="分销 创建并核销",
                content="数据:" + str(data),
                err_obj=str(err_txt)
            )
            return None, err_txt
        except Exception as e:
            write_to_log(
                prefix="分销 创建并核销",
                content="数据:" + str(data),
                err_obj=str(e)
            )
            transaction.savepoint_rollback(sid)
            return None, str(e)

    @staticmethod
    def large_amount_audit(params):
        enroll_id = params.get("enroll_id", "")

        transact_set = Transact.objects.filter(enroll_id=enroll_id, sand_box_status_code="TRANSFERING").first()
        if transact_set:
            return {"status": "1"}, None
        else:
            return {"status": "0"}, None

    # 资金台账
    @staticmethod
    def finance_standing_book(params):
        enroll_id_list = params.get("enroll_id_list", None)
        transact_obj = Transact.objects
        list = []
        for i in enroll_id_list:
            standing_book = {}
            standing_book['enroll_id'] = i  # 报名ID
            standing_book['billing_time'] = None  # 开票时间
            standing_book['charge_time'] = None  # 收款时间时间
            standing_book['charge_mode'] = None  # 收款方式
            standing_book['payment_time'] = None  # 付款时间 （暂无）
            standing_book['payment_delay'] = None  # 付款方式（暂无）
            standing_book['billing_time'] = None  # 开票时间

            transact_set = transact_obj.filter(enroll_id=i, sand_box__isnull=True, ).order_by("-id").first()
            if not transact_set:
                list.append(standing_book)
                continue

            finance_data = transact_set.to_dict()
            pay_mode = PayMode.objects.filter(id=finance_data['pay_mode']).first()
            pay_mode_data = model_to_dict(pay_mode)
            standing_book['charge_time'] = finance_data['transact_time']  # 收款时间时间
            standing_book['charge_mode'] = pay_mode_data['pay_mode']  # 收款方式

            invoice_set = transact_obj.filter(
                sand_box__sand_box_name__in=["BID_SPECIAL_INVOICE", "BID_PLAIN_INVOICE"]
            ).order_by("-id").values("goods_info")
            if not invoice_set:
                continue
            for item in (invoice_set):
                if item['goods_info']:
                    # print(jsLoads)
                    if "enroll" in item['goods_info']:
                        enroll = item['goods_info']['enroll']
                        if isinstance(enroll, dict):
                            if enroll["id"] == i:
                                if 'invoice' in item['goods_info']:
                                    invoice = item['goods_info']['invoice']
                                    billing_time = invoice.get("billing_time", None)
                                    standing_book['billing_time'] = billing_time
                        else:
                            for enroll_item in enroll:
                                if enroll_item["id"] == i:
                                    if 'invoice' in item['goods_info']:
                                        invoice = item['goods_info']['invoice']
                                        billing_time = invoice.get("billing_time", None)
                                        standing_book['billing_time'] = billing_time
            invoiced_amount = float(finance_data['income']) + float(finance_data['outgo'])
            standing_book['invoiced_amount'] = abs(invoiced_amount)  # 发票金额
            list.append(standing_book)

        return list, None

    @staticmethod
    def user_balance_list(params):
        page = int(params['page']) if 'page' in params else 1
        size = int(params['size']) if 'size' in params else 10
        account_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["real_name", "phone"],
            is_remove_empty=True
        )
        order = 0
        account_params["page"] = page
        account_params["size"] = size
        user_list, err = DetailInfoService.get_list_detail(
            params=account_params,
            filter_fields=['user_id', 'user_name', 'register_time', 'real_name', 'nickname', 'phone', 'is_delete'])
        for item in user_list['list']:
            balance = FinanceService.check_balance(account_id=item['user_id'], platform=None,
                                                   platform_id=5, currency='CNY',
                                                   sand_box=None)
            order += 1
            item['order'] = order
            item['balance'] = balance['balance']
            item['account_id'] = item['user_id']
            item['status'] = "使用中" if item.get("is_delete", "") == 0 else "已注销"

        return {'size': int(size), 'page': int(page), 'total': user_list['total'], "list": user_list['list']}, None
