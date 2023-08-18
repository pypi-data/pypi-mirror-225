# _*_coding:utf-8_*_
from django.urls import re_path

from .apis.invoice_apis import InvoiceApi
from .apis.invoice_type_apis import InvoiceTypeApi
from .service_register import register

register()

urlpatterns = [
    re_path(r'^add/?$', InvoiceApi.add, ),  # 发票添加
    re_path(r'^batch_add/?$', InvoiceApi.batch_add, ),  # 发票批量添加
    re_path(r'^edit/?$', InvoiceApi.edit, ),  # 编辑
    re_path(r'^list/?$', InvoiceApi.list, ),  # 列表
    re_path(r'^type_list/?$', InvoiceTypeApi.list, ),  # 列表
    re_path(r'^detail/?$', InvoiceApi.detail, ),  # 详情
    re_path(r'^examine_approve/?$', InvoiceApi.examine_approve, ),  # 发票审批
]
