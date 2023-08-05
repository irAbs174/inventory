from inventory.extensions.jalali_converter import jalali_converter as jConvert, cardex_jalali_converter
from django.db.models import F
from django.db import models


class SiteOrders(models.Model):
    order_code = models.CharField(max_length=40, verbose_name='شماره سفارش',null=False, blank=False )
    full_name = models.CharField(max_length=40, verbose_name='نام کامل',null=False, blank=False )
    phone_number = models.CharField(max_length=40, verbose_name='شماره تلفن',null=False, blank=False )
    package_status = models.BooleanField(default=True, verbose_name='وضعیت بسته', blank=False, null=False)
    send_method = models.CharField(max_length=40, verbose_name='روش ارسال',null=False, blank=False )
    factor_file = models.CharField(max_length=40, verbose_name='فایل pdf',null=False, blank=False )
    order_desc = models.TextField(verbose_name='توضیحات ارسال', db_index=True, null=True, blank=True)
    order_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان دقیق ثبت', null=True, blank=True)

    def jpub(self):
        return jConvert(self.order_time)

    class Meta:
        verbose_name = 'سفارش سایت'
        verbose_name_plural = 'سفارشات سایت'