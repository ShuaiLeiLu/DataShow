# DataShowAPI/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from records import views

urlpatterns = [
    # 管理后台
    path('admin/', admin.site.urls),

    # API接口
    path('api/records/', views.RecordList.as_view(), name='records-list'),
    path('api/upload/', views.FileUploadView.as_view(), name='file-upload'),

    # 自动化API文档
    path('api/docs/', include_docs_urls(title='DataShow API')),

    # 健康检查端点
    path('health/', TemplateView.as_view(template_name='health_check.html'), name='health-check'),

    # 前端入口（需先构建React项目）
    # path('', TemplateView.as_view(template_name='index.html')),
]

# 开发阶段临时欢迎页（可删除）
urlpatterns += [
    path('', lambda request: HttpResponse(
        """
        <h1>DataShow 后端服务运行中</h1>
        <p>可用接口：</p>
        <ul>
            <li><a href="/api/records/">/api/records/</a> - 交易数据接口</li>
            <li><a href="/api/upload/">/api/upload/</a> - 数据上传接口</li>
            <li><a href="/admin/">/admin/</a> - 管理后台</li>
            <li><a href="/api/docs/">/api/docs/</a> - API文档</li>
        </ul>
        """
    ))
]