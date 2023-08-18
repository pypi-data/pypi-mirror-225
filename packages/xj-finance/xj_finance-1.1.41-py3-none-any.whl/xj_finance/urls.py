# _*_coding:utf-8_*_
from django.urls import re_path

from xj_finance.apis.finance_currency_apis import FinanceCurrencyApi
from xj_finance.apis.finance_pay_mode import FinancePayMode
from xj_finance.apis.finance_pay_mode_apis import FinancePayModeApi
from xj_finance.apis.finance_sand_box_apis import FinanceSandBoxApi
from xj_finance.apis.finance_status_code_apis import FinanceStatusCodeApis
from xj_finance.service_register import register
from .apis.finance_apis import FinanceApi
from .apis.finance_labor_apis import FinanceLaborApi
from .apis.finance_ledger_apis import FinanceLedgerApi
from .apis.finance_transacts import FinanceTransacts
from .apis.finance_transact import FinanceTransact
from .apis.finance_currency import FinanceCurrency
from .apis.finance_sand_box import FinanceSandBox
from .apis.finance_statistic import FinanceStatistic
from .apis.finance_status_code import FinanceStatusCode

register()

urlpatterns = [
    re_path(r'^statistic/?$', FinanceStatistic.as_view(), ),

    # API（对外接口）-------------------------------------------------------------------------------------
    # 财务总表
    re_path(r'^transacts/?$', FinanceApi.list, name="财务列表（旧命名）"),
    re_path(r'^transact/?$', FinanceApi.detail, name="财务交详细（旧命名）"),

    re_path(r'^list/?$', FinanceApi.list, name="财务列表"),
    re_path(r'^detail/?$', FinanceApi.detail, name="财务详细"),
    re_path(r'^ledger_related/?$', FinanceApi.ledger_related, name="相关订单详情（台账）"),
    re_path(r'^add/?$', FinanceApi.add, name="财务添加"),
    re_path(r'^edit/?$', FinanceApi.edit, name="财务修改"),
    re_path(r'^balance/?$', FinanceApi.balance, name="获取余额"),
    re_path(r'^cash_withdrawal/?$', FinanceApi.cash_withdrawal, name="财务提现"),
    re_path(r'^large_transfer/?$', FinanceApi.large_transfer, name="大额转账"),
    re_path(r'^examine_approve/?$', FinanceApi.examine_approve, name="财务审批"),
    re_path(r'^large_amount_audit/?$', FinanceApi.large_amount_audit, name="大额转账审核结果查询"),
    re_path(r'^balance_list/?$', FinanceApi.balance_list, name="用户余额列表"),
    re_path(r'^ledger/?$', FinanceLedgerApi.ledger, name="财务台账"),

    # 财务币种表
    re_path(r'^currency/?$', FinanceCurrency.as_view(), ),  # 币种|列表（旧）
    re_path(r'^currency_list/?$', FinanceCurrencyApi.list, name="币种列表"),
    re_path(r'^currency_add/?$', FinanceCurrencyApi.add, name="币种添加"),
    re_path(r'^currency_edit/?$', FinanceCurrencyApi.edit, name="币种修改"),

    # 财务支付方式表
    re_path(r'^pay_mode/?$', FinancePayMode.as_view(), ),
    re_path(r'^pay_mode_list/?$', FinancePayModeApi.list, name="支付方式列表"),
    re_path(r'^pay_mode_add/?$', FinancePayModeApi.add, name="支付方式添加"),
    re_path(r'^pay_mode_edit/?$', FinancePayModeApi.edit, name="支付方式修改"),

    # 财务沙盒表
    re_path(r'^sand_box/?$', FinanceSandBox.as_view(), ),
    re_path(r'^sand_box_list/?$', FinanceSandBoxApi.list, name="沙盒列表"),  # 沙盒列表
    re_path(r'^sand_box_add/?$', FinanceSandBoxApi.add, name="沙盒列表"),  # 沙盒列表
    re_path(r'^sand_box_edit/?$', FinanceSandBoxApi.edit, name="沙盒修改"),  # 沙盒修改

    # 财务付款类型
    re_path(r'^status_code/?$', FinanceStatusCode.as_view(), ),
    re_path(r'^status_code_list/?$', FinanceStatusCodeApis.list, name="付款类型列表"),
    re_path(r'^status_code_add/?$', FinanceStatusCodeApis.add, name="付款类型添加"),
    re_path(r'^status_code_edit/?$', FinanceStatusCodeApis.edit, name="付款类型修改"),

    # 服务（对内测试）-------------------------------------------------------------------------------------

    re_path(r'^create_or_write_off/?$', FinanceTransacts.create_or_write_off, name="财务交易应收应付（服务测试用）"),
    re_path(r'^standing_book/?$', FinanceTransact.finance_standing_book, ),  # 资金台账
    re_path(r'^flow_writing/?$', FinanceTransact.finance_flow_writing, name="分销（服务测试用）"),
    re_path(r'^balance_validation/?$', FinanceTransact.balance_validation, ),

    # 劳务通
    re_path(r'^larbor_add/?$', FinanceLaborApi.larbor_add, name="劳务通写入费用（拆分）"),
]
