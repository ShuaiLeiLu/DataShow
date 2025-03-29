# records/views.py（增强版）
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from .models import TradeRecord
from .serializers import TradeRecordSerializer
import pandas as pd


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