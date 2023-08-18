from orator import DatabaseManager
#
from config.config import JConfig

config = JConfig()
db_config = {
    config.get('main', 'driver', "mysql"): {
        'driver': config.get('main', 'driver', "mysql"),
        'host': config.get('main', 'mysql_host', "127.0.0.1"),
        'database': config.get('main', 'mysql_database', ""),
        'user': config.get('main', 'mysql_user', "root"),
        'password': config.get('main', 'mysql_password', "123456"),
        "port": config.getint('main', 'mysql_port', "3306")
    }
}
db = DatabaseManager(db_config)


class FinanceLedgerV1Service():
    @staticmethod
    def ledger(request_params):
        page = int(request_params.get('page', 1))
        size = int(request_params.get('size', 10))
        customer_code = request_params.get("customer_code", "")
        title = request_params.get("title", "")
        full_name = request_params.get("full_name", "")
        group_id = request_params.get("group_id", "")
        id = 0

        # 第一部分的子查询
        subquery_t1 = db.table('thread as t') \
            .select(
            't.title',
            't.user_id',
            db.raw('u.full_name as full_name'),
            db.raw('t.id as thread_id'),
            db.raw('t.field_6 as customer_code'),
            db.raw('t.field_11 as belonging_region'),
            db.raw('t.field_12 as salesman'),
            db.raw('sum(t.field_1) as total_contract_amount')
        ) \
            .left_join('user_base_info as u', 't.user_id', '=', 'u.id') \
            .where_raw('t.category_id=160') \
            .group_by('t.field_6')

        # 第二部分的子查询
        subquery_t2 = db.table('finance_transact') \
            .select(
            db.raw('field_1 as manage_point'),
            db.raw('field_2 as brokerage_point'),
            db.raw('field_3 as tax_point'),
            db.raw('finance_transact.order_no as customer_code'),
            db.raw('sum(finance_transact.income) as total_amount_received')
        ) \
            .where_null('finance_transact.sand_box_id') \
            .group_by('finance_transact.order_no')

        # 第三部分的子查询
        subquery_t3 = db.table('invoice_invoice as i') \
            .select(
            db.raw('sum(i.invoice_price) as total_invoice_price'),
            db.raw('t.field_6 as customer_code')
        ) \
            .left_join('thread as t', 'i.thread_id', '=', 't.id') \
            .group_by('t.field_6')

        # 主查询
        query = db.table(db.raw(f"({subquery_t1.to_sql()}) as t1")) \
            .select(
            't1.thread_id',
            't1.title',
            't1.user_id',
            'manage_point',
            'brokerage_point',
            'tax_point',
            db.raw('t1.full_name as full_name'),
            db.raw('t1.salesman as salesman'),
            db.raw('t1.customer_code as customer_code'),
            db.raw('t1.belonging_region as belonging_region'),
            db.raw('coalesce(t1.total_contract_amount, 0) as total_contract_amount'),
            db.raw('coalesce(t2.total_amount_received, 0) as total_amount_received'),
            db.raw('coalesce(t3.total_invoice_price, 0) as total_invoice_price'),
            db.raw(
                '(coalesce(t1.total_contract_amount, 0) - coalesce(t3.total_invoice_price, 0)) as project_difference'),
            db.raw(
                '(coalesce(t3.total_invoice_price, 0) - coalesce(t2.total_amount_received, 0)) as accounts_receivable')
        ) \
            .left_join(db.raw(f"({subquery_t2.to_sql()}) as t2"), 't1.customer_code', '=', 't2.customer_code') \
            .left_join(db.raw(f"({subquery_t3.to_sql()}) as t3"), 't1.customer_code', '=', 't3.customer_code')
        group_query = db.table('role_user_to_group').select('user_id').where('user_group_id', group_id).get()
        user_ids = [item['user_id'] for item in group_query]
        if user_ids:
            query.where_in('user_id', user_ids)
        else:
            query.where_null('user_id')

        if customer_code:
            query.where('t1.customer_code', '=', customer_code)
        if title:
            query.where('t1.title', 'like', f'%{title}%')
        if full_name:
            query.where('t1.full_name', 'like', f'%{full_name}%')

        total = query.get().count()

        results = query.paginate(size, page)
        results_list = results.items
        # print(results)
        # print(query.to_sql())
        return {'size': size, 'page': page + 1, 'total': total, 'list': results_list}, None
