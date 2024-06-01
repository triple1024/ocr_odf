from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('open/', views.open_pdf, name='open_pdf'),
    path('extract/', views.upload_pdf_page, name='upload_pdf_page'),  # 新しいビューを追加
    path('extract_text/', views.extract_text_from_uploaded_pdf, name='extract_text_from_uploaded_pdf'),
    path('my_view/', views.my_view, name='my_view'),
]
