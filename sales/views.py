from django.shortcuts import render
from django.db.models import Sum, F
from customers.models import OrderItem
from menu.models import MenuItem

def sales_report(request):
    total_sales = OrderItem.objects.aggregate(total_sales=Sum(F('quantity') * F('menu_item__price')))['total_sales'] or 0

    sales_by_item = MenuItem.objects.annotate(
        total_revenue=Sum(F('orderitem__quantity') * F('price'))
    ).filter(total_revenue__gt=0).order_by('-total_revenue')

    return render(request, 'sales/sales_report.html', {
        'total_sales': total_sales,
        'sales_by_item': sales_by_item
    })