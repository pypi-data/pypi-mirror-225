# _*_coding:utf-8_*_

import os, logging, time, json, copy

from rest_framework.decorators import api_view
from rest_framework.views import APIView

from xj_finance.utils.utility_method import extract_values, replace_key_in_dict, replace_key_in_list_dicts, \
    replace_key_in_dict_replacement_dicts
from xj_thread.services.thread_list_service import ThreadListService
from xj_user.services.user_detail_info_service import DetailInfoService
from xj_user.services.user_service import UserService
from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper, format_params_handle
from xj_finance.services.finance_transact_service import FinanceTransactService
from xj_finance.services.finance_transacts_service import FinanceTransactsService
from xj_finance.services.finance_list_service import FinanceListService
from xj_finance.utils.user_wrapper import user_authentication_wrapper
from ..utils.model_handle import util_response
from ..services.finance_service import FinanceService

logger = logging.getLogger(__name__)


class FinanceApi(APIView):  # 或继承(APIView)

    # 财务添加
    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def add(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        platform_id = user_info.get("platform_id")
        params.setdefault("account_id", user_id)  # 用户ID
        transact_set, err = FinanceTransactService.add(params)
        if err is None:
            return util_response(data=transact_set)
        return util_response(err=47767, msg=err)

    # 财务修改
    @api_view(['PUT'])
    @user_authentication_wrapper
    @request_params_wrapper
    def edit(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        platform_id = user_info.get("platform_id")
        params.setdefault("account_id", user_id)  # 用户ID
        transact_set, err = FinanceTransactService.add(params)
        if err is None:
            return util_response(data=transact_set)
        return util_response(err=47767, msg=err)

    # 财务列表
    @api_view(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def list(self, *args, user_info, request_params, **kwargs, ):
        if request_params is None:
            request_params = {}
        if user_info:
            request_params.setdefault("user_id", user_info.get("user_id"))
        else:
            return util_response(err=6001, msg="非法请求，请您登录")

        filter_fields = request_params.get("filter_fields", None)

        # ================== 信息id列表反查询报名 start===============================
        thread_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=["title", "subtitle", "access_level", "author"],
            is_remove_empty=True
        )
        if thread_params:
            thread_ids, err = ThreadListService.search_ids(search_prams=thread_params)
            if not err:
                request_params["thread_id_list"] = thread_ids

            if isinstance(request_params.get("thread_id_list"), list) and len(
                    request_params["thread_id_list"]) == 0:
                request_params["thread_id_list"] = [0]
        # ================== 信息id列表反查询报名 end ===============================

        # ================== 用户id列表反查询报名 start===============================
        account_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=["account_name", 'real_name'],
            is_remove_empty=True
        )

        if account_params:
            print(account_params)
            account_ids, err = UserService.user_list(
                params=replace_key_in_dict_replacement_dicts(account_params, {"account_name": "user_name"}))
            if not err:
                print(account_ids)
                request_params["account_id_list"] = extract_values(account_ids['list'], 'user_id')

            if isinstance(request_params.get("account_id_list"), list) and len(
                    request_params["account_id_list"]) == 0:
                request_params["account_id_list"] = [0]
        # ================== 用户id列表反查询报名 end ===============================

        # ================== 对方用户id列表反查询报名 start===============================
        their_account_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=["their_account_name", "their_real_name", "their_nickname"],
            is_remove_empty=True
        )
        if their_account_params:
            their_account_ids, err = UserService.user_list(
                params=replace_key_in_dict_replacement_dicts(their_account_params,
                                                             {"their_account_name": "user_name", "their_real_name":
                                                                 "real_name", "their_nickname": "nickname"}))
            if not err:
                request_params["their_account_id_list"] = extract_values(their_account_ids['list'], 'user_id')

            if isinstance(request_params.get("their_account_id_list"), list) and len(
                    request_params["their_account_id_list"]) == 0:
                request_params["their_account_id_list"] = [0]
        # ================== 对方用户id列表反查询报名 end ===============================

        transact_set, err = FinanceListService.list(request_params, user_info.get("user_id"), filter_fields)

        if err is None:
            return util_response(data=transact_set)

        return util_response(err=47767, msg=err)

    # 财务详细
    @api_view(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def detail(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        # ============   字段验证处理 start ============
        user_id = user_info.get("user_id")
        params.setdefault("user_id", user_id)  # 用户ID
        transact_set, err = FinanceListService.detail(params.get("finance_id", 0), params.get("order_no", ""))
        # transact_set, err = FinanceListService.detail(params.get("finance_id", 0))
        if err is None:
            return util_response(data=transact_set)
        return util_response(err=47767, msg=err)

    # 财务台账关联
    @api_view(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def ledger_related(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        # ============   字段验证处理 start ============
        user_id = user_info.get("user_id")
        params.setdefault("user_id", user_id)  # 用户ID
        transact_set, err = FinanceListService.detail_all(params.get("order_no", None), params.get("is_ledger", None))
        if err is None:
            return util_response(data=transact_set)
        return util_response(err=47767, msg=err)

    # 查询余额
    @api_view(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def balance(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        # ============   字段验证处理 start ============
        user_id = user_info.get("user_id")
        platform_id = user_info.get("platform_id")
        data = FinanceService.check_balance(account_id=user_id, platform=None,
                                            platform_id=platform_id, currency='CNY',
                                            sand_box=None)
        return util_response(data=data)

    # 查询余额
    @api_view(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def balance_list(self, *args, user_info, request_params, **kwargs, ):
        if request_params is None:
            request_params = {}
        if user_info:
            request_params.setdefault("user_id", user_info.get("user_id"))
        else:
            return util_response(err=6001, msg="非法请求，请您登录")
        # ================== 用户id列表反查询报名 start===============================
        account_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=["real_name", "phone"],
            is_remove_empty=True
        )
        if account_params:
            account_ids, err = DetailInfoService.get_list_detail(
                params=account_params)
            if not err:
                request_params["account_id_list"] = extract_values(account_ids['list'], 'user_id')

            if isinstance(request_params.get("account_id_list"), list) and len(
                    request_params["account_id_list"]) == 0:
                request_params["account_id_list"] = [0]
        # ================== 用户id列表反查询报名 end ===============================

        # ============   字段验证处理 start ============
        data, err = FinanceListService.user_balance_list(request_params)
        if err is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err)

    # 财务提现
    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def cash_withdrawal(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        platform_id = user_info.get("platform_id")
        params.setdefault("account_id", user_id)  # 用户ID
        cash_withdrawal_set, err = FinanceTransactService.finance_flow_writing(params=params, finance_type='WITHDRAW')
        if err is None:
            return util_response(data=cash_withdrawal_set)
        return util_response(err=47767, msg=err)

    # 大额转账
    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    @flow_service_wrapper
    def large_transfer(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        platform_id = user_info.get("platform_id")
        params.setdefault("account_id", user_id)  # 用户ID
        data, err_txt = FinanceTransactService.finance_flow_writing(params=params, finance_type='OFFLINE')
        if err_txt is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)

    # 财务审批（核销、红冲、提现状态、转账）
    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    @flow_service_wrapper
    def examine_approve(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        platform_id = user_info.get("platform_id")
        params.setdefault("account_id", user_id)  # 用户ID
        data, err_txt = FinanceListService.examine_approve(params)
        if err_txt is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err_txt)

    # 大额转账审核结果查询
    @api_view(['GET'])
    @user_authentication_wrapper
    @request_params_wrapper
    def large_amount_audit(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        params.setdefault("account_id", user_id)  # 用户ID
        transact_set, err = FinanceListService.large_amount_audit(params)
        if err is None:
            return util_response(data=transact_set)
        return util_response(err=47767, msg=err)
