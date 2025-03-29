# records/models.py（最终确认版）
from django.db import models

class TradeRecord(models.Model):
    trade_date = models.DateField(verbose_name="交易日期")
    symbol = models.CharField(max_length=20, verbose_name="交易品种")
    entry_point = models.DecimalField(
        max_digits=12, 
        decimal_places=4,  # 适应更精确的金融数据
        verbose_name="开仓点位"
    )
    is_success = models.BooleanField(default=False, verbose_name="开仓成功")
    is_profit = models.BooleanField(default=False, verbose_name="是否盈利")

    class Meta:
        ordering = ['-trade_date']  # 默认按日期倒序排列
        verbose_name = "交易记录"
        verbose_name_plural = "交易记录"