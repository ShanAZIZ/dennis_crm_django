from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
# Create your views here.
from .models import *
from .forms import OrderForm
from .filters import OrderFilter

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='pending').count()
    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders
    }
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context)


def customer(request, pk):
    oneCustomer = Customer.objects.get(id=pk)
    orders = oneCustomer.order_set.all()
    orders_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        'customer': oneCustomer,
        'orders': orders,
        'orders_count': orders_count,
        'myFilter': myFilter
    }
    return render(request, 'accounts/customer.html', context)


def createOrders(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=3)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        #print('Printing POST : ', request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {
        'formset': formset,
        'customer': customer
    }
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    context = {
        'form': form
    }
    if request.method == 'POST':
        print('Printing POST : ', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):
    item = Order.objects.get(id=pk)
    context = {
        'item': item
    }
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    return render(request, 'accounts/delete.html', context)