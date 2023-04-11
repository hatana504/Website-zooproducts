from cart.forms import CartAddProductForm
from django.shortcuts import render, get_object_or_404

from .filters import ProductFilter
from .models import Product, Type


def product_list(request, type_slug=None):
    type = None
    types = Type.objects.all()
    products = Product.objects.filter(available=True)
    if type_slug:
        type = get_object_or_404(Type, slug=type_slug)
        products = products.filter(type=type)

    f = ProductFilter(request.GET, queryset=Product.objects.all())
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    context = {
        'type': type,
        'types': types,
        'products': products,
        'filter': f,
        'has_filter': has_filter
    }
    return render(request,
                  'catalog/product/list.html',
                  context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }
    return render(request,
                  'catalog/product/detail.html',
                  context)
