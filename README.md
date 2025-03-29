DataShow 后端服务文档
项目概述
基于Django的金融交易数据管理系统，提供标准化的API接口支持，采用RESTful架构设计，支持数据存储、查询和批量上传功能。

架构图

功能特性
功能模块	实现状态	技术方案
数据存储	✅	Django ORM + MySQL
数据查询API	✅	DRF + 分页/过滤
CSV数据导入	✅	Pandas解析 + 批量创建
基础统计指标	✅	动态查询集计算
跨域支持	✅	django-cors-headers
自动化API文档	✅	DRF Schema + CoreAPI
技术栈
核心框架: Django 4.2 + Django REST Framework 3.14

# API文档
# 接口列表
端点	方法	功能	示例请求体

/api/records/	GET	获取分页交易记录	?page=2&symbol=BTC/USDT

/api/upload/	POST	上传CSV文件	form-data: file=@data.csv

/api/stats/	GET	获取近30日统计指标	-

复制
# 获取交易记录
curl -X GET "http://localhost:8000/api/records/?page_size=5" 

# 上传数据文件
curl -X POST -F "file=@sample_data.csv" http://localhost:8000/api/upload/

# 获取统计数据
curl -X GET "http://localhost:8000/api/stats/"
响应示例
json
复制
{
  "start_date": "2023-07-01",
  "end_date": "2023-07-31",
  "total_orders": 85,
  "opened_orders": 72,
  "open_rate": 0.8471,
  "profit_rate": 0.6389
}


许可证
MIT License © 2025
