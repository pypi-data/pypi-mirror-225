from django.db import connection

from xj_finance.utils.utility_method import aggregate_data
from xj_thread.services.thread_list_service import ThreadListService


class FinanceLedgerService:
    @staticmethod
    def ledger(request_params):
        where_clauses = []
        page = int(request_params['page']) - 1 if 'page' in request_params else 0
        size = int(request_params['size']) if 'size' in request_params else 10
        customer_code = request_params.get("customer_code", "")
        title = request_params.get("title", "")
        full_name = request_params.get("full_name", "")
        group_id = request_params.get("group_id", "")
        query = f"SELECT * FROM finance_ledger_view"
        group_query = f"SELECT user_id FROM role_user_to_group where user_group_id = '{group_id}'"
        user_list = FinanceLedgerService.execute_raw_sql(group_query)
        user_ids = [item['user_id'] for item in user_list]
        if user_ids:
            user_ids_str = ",".join(str(user_id) for user_id in user_ids)
            where_clauses.append(f"user_id IN ({user_ids_str})")
        else:
            where_clauses.append(f"user_id IS NULL")

        if customer_code:
            where_clauses.append(f"customer_code = '{customer_code}'")
        if title:
            where_clauses.append(f"title LIKE '%{title}%'")
        if full_name:
            where_clauses.append(f"full_name LIKE '%{full_name}%'")
        # 拼接WHERE条件
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        # 添加分页部分
        total = len(FinanceLedgerService.execute_raw_sql(query))

        query += f" LIMIT {size} OFFSET {page * size};"
        results_list = FinanceLedgerService.execute_raw_sql(query)
        print(query)
        # 将结果输出到控制台，使用UTF-8编码
        # for item in results_list:
        #     print(item.get("customer_code"))
        return {'size': int(size), 'page': int(page + 1), 'total': total, 'list': results_list}, None

    @staticmethod
    def execute_raw_sql(query):
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return results
