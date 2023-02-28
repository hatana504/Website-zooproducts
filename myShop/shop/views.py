from django.db.models import Q, CharField, Value
from django.db.models.functions import Concat
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from .models import Customer, Order


class HomePageView(TemplateView):
    template_name = 'home.html'


class CustomersListView(ListView):
    template_name = "customers.html"
    model = Customer
    context_object_name = "list_of_all_customers"


class OrdersListView(ListView):
    template_name = "orders.html"
    model = Order
    context_object_name = "list_of_all_orders"

    @staticmethod
    def all_customers():
        return Customer.objects.all()


class SearchView(ListView):
    template_name = "search.html"
    model = Order
    context_object_name = "list_of_all_orders"

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset().order_by('order_date').reverse()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.annotate(
                full_name=Concat(
                    'customer__first_name',
                    Value(' '),
                    'customer__last_name',
                    output_field=CharField()
                )
            ).filter(
                Q(full_name__icontains=query) |
                Q(customer__first_name__iexact=query) |
                Q(customer__last_name__iexact=query)
            )
        return queryset

