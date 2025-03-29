# records/views.py（增强版）
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from .serializers import TradeRecordSerializer
import pandas as pd
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TradeRecord
class RecordList(generics.ListCreateAPIView):
    queryset = TradeRecord.objects.all()
    serializer_class = TradeRecordSerializer
    filterset_fields = {  # 添加过滤功能
        'trade_date': ['exact', 'gte', 'lte'],
        'symbol': ['exact'],
        'is_success': ['exact'],
        'is_profit': ['exact']
    }


class FileUploadView(generics.CreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = TradeRecordSerializer

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']
        try:
            df = pd.read_csv(file_obj)
            # 数据清洗与校验
            df['trade_date'] = pd.to_datetime(df['trade_date']).dt.date
            records = df.to_dict('records')

            created = []
            for record in records:
                obj, _ = TradeRecord.objects.update_or_create(
                    trade_date=record['trade_date'],
                    symbol=record['symbol'],
                    defaults=record
                )
                created.append(obj.id)

            return Response({
                "status": "success",
                "created_records": len(created)
            }, status=201)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=400)


class TradeStatsView(APIView):
    def get(self, request):
        # 计算时间范围
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)

        # 基础查询集
        queryset = TradeRecord.objects.filter(
            trade_date__gte=start_date,
            trade_date__lte=end_date
        )

        # 计算各项指标
        total_orders = queryset.count()
        opened_orders = queryset.filter(is_success=True).count()

        success_queryset = queryset.filter(is_success=True)
        profitable_orders = success_queryset.filter(is_profit=True).count()

        # 计算比率（避免除零错误）
        open_rate = opened_orders / total_orders if total_orders > 0 else 0
        profit_rate = profitable_orders / opened_orders if opened_orders > 0 else 0

        return Response({
            "start_date": start_date,
            "end_date": end_date,
            "total_orders": total_orders,
            "opened_orders": opened_orders,
            "open_rate": round(open_rate, 4),
            "profit_rate": round(profit_rate, 4)
        })
