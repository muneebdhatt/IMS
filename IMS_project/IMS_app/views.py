from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Order,Orderitem,Product
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models import Sum, F
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.db.models import Sum, F
from django.db.models.functions import TruncDate
# Create your views here.

def index(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()
    orderitem = Orderitem.objects.all()
    return render(request , 'index.html', {'customers': customers, 'products': products, 'orders': orders, 'orderitem': orderitem})

def list_all_orders(request):
    order_list = Order.objects.all()
    paginator = Paginator(order_list, 10)
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    
    return render(request, 'orders.html', {'orders': orders})

def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    customers = Customer.objects.all()
    products = Product.objects.all()
    
    if request.method == 'POST':
        try:
            # Update customer
            customer_id = request.POST['customer']
            order.customer = Customer.objects.get(id=customer_id)
            order.save()
            
            # Delete existing order items
            order.orderitem_set.all().delete()
            
            # Create new order items
            for product in products:
                quantity = int(request.POST.get(f"quantity_{product.id}", 0))
                if quantity > 0:
                    Orderitem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity
                    )
            
            messages.success(request, f'Order #{order.id} has been updated successfully.')
            return redirect('invoice_view', order_id=order.id)
            
        except Exception as e:
            messages.error(request, f'Error updating order: {str(e)}')
            return redirect('update_order', order_id=order.id)
    
    return render(request, 'update_order.html', {
        'order': order,
        'customers': customers,
        'products': products
    })

def delete_orders(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()  # This will also delete related OrderItems due to CASCADE
    return redirect('all_orders')  # Redirect back to the orders list page

def products_view(request):
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Get all products
    products_list = Product.objects.all()
    
    # Apply search filter if query exists
    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    return render(request, 'products.html', {
        'products': products,
        'search_query': search_query
    })


def create_order(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    
    if request.method == 'POST':
        customer_id = request.POST['customer']
        customer = Customer.objects.get(id=customer_id)
        order = Order.objects.create(customer=customer)
        
        for product in products:
            quantity = int(request.POST.get(f"quantity_{product.id}", 0))
            if quantity > 0:
                Orderitem.objects.create(order=order, product=product, quantity=quantity)
                
        return redirect('invoice_view', order_id = order.id)
    
    return render(request, 'create_order.html', {'customers': customers, 'products':products})




def invoice_view(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'invoice.html', {'order':order})


def export_invoice_pdf(request, order_id):
    order = Order.objects.get(id=order_id)
    html_string = render_to_string('invoice.html', {'order': order})
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=invoice_{order.id}.pdf'
    html.write_pdf(response)
    return response




def sales_report(request):
    report = (
        Orderitem.objects.annotate(
            date=TruncDate('order__orderdate')
        )
        .values('date')
        .annotate(total=Sum(F('quantity') * F('product__price')))
        .order_by('date')
    )

    total_sales = sum(r['total'] for r in report)
    count = len(report)
    average_sales = total_sales / count if count else 0

    return render(request, 'sales_report.html', {
        'report': report,
        'total_sales': total_sales,
        'average_sales': average_sales,
    })



def search_orders(request):
    query = request.GET.get('q', '')
    orders = Order.objects.all()
    
    if query:
        orders = Order.objects.filter(
            Q(customer__name__icontains = query) |
            Q(id__icontains=query) |
            Q(orderdate__icontains=query))
        
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    return render(request, 'search.html', {'orders':orders, 'query':query})

def products_view(request):
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Get all products
    products_list = Product.objects.all()
    
    # Apply search filter if query exists
    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    return render(request, 'product.html', {
        'products': products,
        'search_query': search_query
    })