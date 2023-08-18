# encoding: utf-8
"""
@project: djangoModel->extend_service
@author:高栋天
@Email: sky4834@163.com
@synopsis: 扩展服务
@created_time: 2022/7/29 15:14
"""
from django.db.models import F

from ..models import Transact, FinanceExtendData, FinanceMainExtendField, FinanceExtendField
from ..utils.custom_tool import write_to_log, force_transform_type, filter_result_field, format_params_handle


# 扩展字段增删改查
class FianceExtendService:
    @staticmethod
    def create_or_update(params=None, finance_id=None, sand_box_id=None, **kwargs):
        """
        信息表扩展信息新增或者修改
        :param params: 扩展信息，必填
        :param finance_id: 财务ID，必填
        :param sand_box_id: 沙盒ID, 非必填
        :return: None，err
        """
        # 参数合并，强制类型转换
        kwargs, is_void = force_transform_type(variable=kwargs, var_type="dict", default={})
        params, is_void = force_transform_type(variable=params, var_type="dict", default={})
        params.update(kwargs)

        # 不存在信息ID 无法修改
        finance_id = finance_id or params.pop("finance_id", None)
        finance_id, is_void = force_transform_type(variable=finance_id, var_type="int")
        if finance_id is None:
            return None, "扩展字段修改错误,finance_id不可以为空"

        # 检查信息ID 是否正确
        Transact_obj = Transact.objects.filter(id=finance_id).first()
        if not Transact_obj:
            return None, "没有找到该主表信息，无法添加扩展信息"
        # 获取沙盒类别ID 当没有指定沙盒分类的时候，则不可以添加或者修改扩展数据。因为扩展字段于沙盒绑定。
        sand_box_id = sand_box_id if sand_box_id else Transact_obj.sand_box_id
        if not sand_box_id:
            return None, "没有信息指定砂灰色类别，无法添加扩展信息"

        # 扩展字段映射, 如没有配置对应类别的扩展字段，则无法添加扩展数据。
        extend_fields = FinanceExtendField.objects.filter(sand_box_id=sand_box_id).values("field_index",
                                                                                          "default",
                                                                                          "field")
        if not extend_fields:
            return None, "没有配置扩展该类别的扩展字段，无法添加扩展信息"

        extend_model_fields = [i.name for i in FinanceExtendData._meta.fields if
                               not i.name == "finance_id"]  # 扩展信息表的字段列表
        # 扩展数据替换
        extend_field_map = {item["field"]: item["field_index"] for item in extend_fields if
                            item["field_index"] in extend_model_fields}  # 得到合理的配置
        transformed_extend_params = {extend_field_map[k]: v for k, v in params.items() if
                                     extend_field_map.get(k)}  # {"自定义扩展字段":"123"} ==>> {"filed_1":"123"}
        # 修改或添加数据
        try:
            extend_obj = FinanceExtendData.objects.filter(finance_id=finance_id)
            if not extend_obj:
                # 新增的时候，启用扩展字段参数设置默认值。
                # 注意：防止后台管理员配置错误,出现数据表不存在的字段。所以需要进行一次字段排除
                default_field_map = {item["field_index"]: item["default"] for item in extend_fields if
                                     (item["default"] and item["field_index"] in extend_model_fields)}
                for field_index, default in default_field_map.items():
                    transformed_extend_params.setdefault(field_index, default)
                if not transformed_extend_params:
                    return None, "没有可添加的数据，请检查扩展字段的默认值配置"

                # 添加扩展信息
                transformed_extend_params.setdefault('finance_id_id', finance_id)
                FinanceExtendData.objects.create(**transformed_extend_params)
                return None, None
            else:
                if not transformed_extend_params:
                    return None, "没有可修改的数据"

                extend_obj.update(**transformed_extend_params)
                return None, None
        except Exception as e:
            write_to_log(prefix="信息表扩展信息新增或者修改异常", err_obj=e)
            return None, "信息表扩展信息新增或者修改异常:" + str(e)

    @staticmethod
    def get_extend_info(finance_id_list: list = None):
        """
        获取映射后的扩展数据
        :param finance_id_list: 财务ID列表
        :return: extend_list, err
        """
        # 参数类型校验
        finance_id_list, is_void = force_transform_type(variable=finance_id_list, var_type="list")
        if not finance_id_list:
            return [], None

        # 信息与类别映射
        Transact_sand_box_list = list(Transact.objects.filter(id__in=finance_id_list).values("id", "sand_box_id"))
        Transact_sand_box_map = {i["id"]: i["sand_box_id"] for i in Transact_sand_box_list if
                                 i.get("sand_box_id", None)}

        # 扩展字段映射, 如没有配置对应类别的扩展字段，则无法添加扩展数据。
        extend_fields = list(FinanceExtendField.objects.values("sand_box_id", "field_index", "field"))
        if not extend_fields:
            return [], None
        extend_field_map = {}
        for item in extend_fields:
            if extend_field_map.get(item["sand_box_id"]):
                extend_field_map[item["sand_box_id"]].update({item["field_index"]: item["field"]})
            else:
                extend_field_map[item["sand_box_id"]] = {item["field_index"]: item["field"],
                                                         "finance_id_id": "finance_id"}
        # 查询出扩展原始数据
        try:
            Transact_extend_list = list(FinanceExtendData.objects.filter(finance_id__in=finance_id_list).values())
        except Exception as e:
            return [], "获取扩展数据异常"
        # 处理获取到结果，字段替换
        try:
            finish_list = []
            for i in Transact_extend_list:
                # 查看该条信息是否指定sand_box_id，没有则跳过
                current_sand_box_id = Transact_sand_box_map.get(i["finance_id_id"], None)
                if not current_sand_box_id:
                    continue
                # 如果该类别没有配置扩展字段则跳过
                current_extend_fields = extend_field_map.get(current_sand_box_id, {})
                if not current_extend_fields:
                    continue
                # 进行替换
                finish_list.append(format_params_handle(
                    param_dict=i,
                    alias_dict=current_extend_fields,
                    is_remove_null=False
                ))
            # 剔除不需要的字段
            finish_list = filter_result_field(
                result_list=finish_list,
                remove_filed_list=[i.name for i in FinanceExtendData._meta.fields if not i.name == "finance_id"]
            )
            return finish_list, None

        except Exception as e:
            write_to_log(prefix="获取映射后的扩展数据,数据拼接异常", err_obj=e,
                         content="finance_id_list:" + str(finance_id_list))
            return [], None

    @staticmethod
    def create_or_update_main(params: dict = None, **kwargs):
        """
        添加或修改财务主表的详细信息
        :param params: 添加/修改参数
        :return: None,err_msg
        """
        # 参数判断
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="dict", default={})
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        params.update(kwargs)
        finance_id, is_pass = force_transform_type(variable=params.pop('finance_id', None), var_type="int")
        if not finance_id:
            return None, "参数错误,finance_id"
        # 判断用户是否存在
        finance_base = Transact.objects.filter(id=finance_id)
        finance_base_info = finance_base.first()
        if not finance_base_info:
            return None, '资金记录不存在'
        # =========== section 获取扩展字段的映射，默认值 start =================
        extend_field_list = FinanceMainExtendField.objects.all().values("field", 'field_index', 'default')
        alias_dict = {item['field']: item['field_index'] for item in extend_field_list}  # 字段还原映射字典
        default_map = {item['field_index']: item['default'] for item in extend_field_list if
                       not item['default'] is None}  # 默认字段
        filter_filed_list = [i.name for i in Transact._meta.fields]  # 字段列表
        # 强制类型转换,防止修改报错
        filter_filed_list.remove("id")
        # =========== section 获取扩展字段的映射，默认值 end   =================

        # =========== section 把扩展字段还原成 start =================
        # 剔除掉不是配置的扩展字段,还有原表的字段
        transformed_params = format_params_handle(
            param_dict=format_params_handle(
                param_dict=params,
                alias_dict=alias_dict
            ),
            filter_filed_list=filter_filed_list,
        )
        # print(transformed_params)
        transformed_params.setdefault("id", finance_id)
        # print(detail_user_obj)
        # print("transformed_params >>>", transformed_params)
        # =========== section 把扩展字段还原成 end   =================

        # =========== section 进行数据库操作 start ============
        # try:
        # 判断是否添加过
        detail_user_obj = Transact.objects.filter(id=finance_id)
        if not detail_user_obj.first():
            # 没有添加，进行添加操作
            transformed_params.pop("id", None)  # 添加的时候不能有ID主键，防止主键冲突
            # 在添加的时候给字段默认值
            for field_index, default in default_map.items():
                transformed_params.setdefault(field_index, default)

            Transact.objects.create(**transformed_params)
        else:
            # 添加过进行跟新
            detail_user_obj.update(**transformed_params)
        return None, None
        # except Exception as e:
        #     return None, "参数配置错误：" + str(e)
        # =========== section 进行数据库操作 end   ============

    @staticmethod
    def get_extend_fields():
        """
        获取用户表扩展字段，前端渲染使用
        :return: fields_list,None
        """
        fields = FinanceMainExtendField.objects.order_by("-sort").all().to_json()
        return fields, None


# 主表扩展字段增删改查
class FinanceMainExtendService:
    int_extend_fields = ["field_1", "field_2", "field_3", "field_4", "field_5"]
    char_extend_fields = ["field_6", "field_7", "field_8", "field_9", "field_10"]
    all_main_extend_fields = int_extend_fields + char_extend_fields
    extend_fields = []

    def __init__(self, sand_box_id, finance_id=None):
        # 获取扩展字段
        sand_box_id, err = force_transform_type(variable=sand_box_id, var_type="int")
        if not sand_box_id:
            self.extend_fields = []
        else:
            self.extend_fields = list(FinanceMainExtendField.objects.filter(sand_box_id=sand_box_id).values(
                "id", "sand_box_id", "field", "field_index", "value", "type", "unit", "config", "default"
            ))

    def format_params_beforehand(self):
        """
        数据过滤预先处理
        :return:(filter_filed_list,alias_dict), err_info
        """
        # 获取过滤字段以及映射字典
        alias_dict = {}
        filter_filed_list = []
        for i in self.extend_fields:
            if not i["field_index"] in FinanceMainExtendField.all_main_extend_fields:
                continue
            filter_filed_key = i["field"] + (
                "|int" if i["field_index"] in FinanceMainExtendField.int_extend_fields else "|str")
            filter_filed_list.append(filter_filed_key)
            alias_dict[i["field"]] = i["field_index"]
        return (filter_filed_list, alias_dict), None

    def validate(self, params: dict):
        """
        验证长度验证，默认值处理
        :return: params
        """
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        if err:
            return params, err

        field_map = {i["field_index"]: i for i in self.extend_fields if
                     i["field_index"] in FinanceMainExtendField.all_main_extend_fields}
        for field_index, map in field_map.items():
            # 判断字符串字段是否超出长度
            if params.get(field_index) and field_index in self.char_extend_fields and len(
                    params.get(field_index)) > 255:
                return None, (map.get("field") + " 长度不可以超过255个字符串")

            # 如果该字段为空或者未传，又配置了扩展字段德默认值，则字段进行赋值
            elif (not params.get(field_index) and map.get("default")):
                params[field_index] = map.get("default")

        return params, None

    @staticmethod
    def replace_list_extend(result_list: list):
        """
        转换主表的扩展字段
        :param result_list: 列表字典
        :return: data,err
        """
        try:
            main_extend_list = list(FinanceMainExtendField.objects.all().values(
                "id", "sand_box_id", "field", "field_index", "value", "type", "unit", "config", "default"
            ))
            main_extend_category_map = {}
            for i in main_extend_list:
                if not main_extend_category_map.get(i["sand_box_id"]):
                    main_extend_category_map[i["sand_box_id"]] = {i["field_index"]: i["field"]}
                else:
                    main_extend_category_map[i["sand_box_id"]][i["field_index"]] = i["field"]

            new_result_list = []
            for result in result_list:
                result = format_params_handle(
                    param_dict=result,
                    alias_dict=main_extend_category_map.get(result["sand_box_id"], {})
                )
                result = format_params_handle(
                    param_dict=result,
                    remove_filed_list=FinanceMainExtendField.all_main_extend_fields
                )
                new_result_list.append(result)
            return new_result_list, None

        except Exception as e:
            return result_list, str(e)
