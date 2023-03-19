from cart.forms import CartAddProductForm
from catalog.models import Product
from django.http import JsonResponse
from django.shortcuts import render, redirect


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def favorites_list(request):
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    context = {'products': products,
               'cart_product_form': cart_product_form}
    return render(request, 'favorites/list.html', context)


def favorites_add(request):
    if request.method == 'POST':
        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
            request.session['favorites'] = list(request.session['favorites'])
        item_exist = next((item for item in request.session['favorites'] if item['id'] == request.POST.get('id')),
                          False)
        add_data = {
            'id': request.POST.get('id'),
        }
        if not item_exist:
            request.session['favorites'].append(add_data)
            request.session.modified = True

        if is_ajax(request):
            data = {
                'id': request.POST.get('id'),
            }
            request.session.modified = True
            return JsonResponse(data)
    return redirect(request.POST.get('url_from'))


def favorites_remove(request):
    if request.method == 'POST':
        for item in request.session['favorites']:
            if item['id'] == request.POST.get('id'):
                item.clear()
        while {} in request.session['favorites']:
            request.session['favorites'].remove({})
        if not request.session['favorites']:
            del request.session['favorites']
        request.session.modified = True

        if is_ajax(request):
            data = {
                'id': request.POST.get('id'),
            }
            request.session.modified = True
            return JsonResponse(data)
    return redirect(request.POST.get('url_from'))


def favorites_list_remove(request, id):
    if request.method == 'POST':
        for item in request.session['favorites']:
            if item['id'] == id:
                item.clear()
        while {} in request.session['favorites']:
            request.session['favorites'].remove({})
        if not request.session['favorites']:
            del request.session['favorites']
        request.session.modified = True
    return redirect(request.POST.get('url_from'))


def favorites_api(request):
    return JsonResponse(request.session.get('favorites'), safe=False)
