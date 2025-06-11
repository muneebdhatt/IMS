from django.contrib import admin
from django.urls import path, include
from . import views
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO
urlpatterns = [
    path('', views.index, name='index'),
    path('create_order/', views.create_order, name='create_order'),
    path('invoice_id/<int:order_id>/', views.invoice_view, name='invoice_view'),
    path('invoice_id/<int:order_id>/pdf', views.export_invoice_pdf, name='export_invoice_pdf'),
    path('sales_report', views.sales_report, name='sales_report'),
    path('search', views.search_orders, name='search_orders'),
    path('products/', views.products_view, name='products'),
    path('all_orders/', views.list_all_orders, name='all_orders'),
    path('delete/<int:order_id>', views.delete_orders, name='delete'),
    path('update_order/<int:order_id>/', views.update_order, name='update_order'),
]
