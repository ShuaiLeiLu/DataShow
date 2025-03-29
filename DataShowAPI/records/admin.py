# records/admin.py
from django.contrib import admin
from .models import TradeRecord
from django.contrib.auth.models import Group, User

# 取消注册默认模型
admin.site.unregister(Group)
admin.site.unregister(User)
@admin.register(TradeRecord)
class TradeRecordAdmin(admin.ModelAdmin):
    list_display = [
        'trade_date', 
        'symbol',
        'entry_point',
        'is_success',
        'is_profit'
    ]
    list_filter = ['trade_date', 'symbol']
    search_fields = ['symbol']
    date_hierarchy = 'trade_date'