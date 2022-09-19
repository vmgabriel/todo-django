"""Django Views"""

# Libraries
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.conf import settings

# Modules
from . import forms, models
from products import models as product_models
from socials.utils import telegram


class ToBuyHomeView(generic.TemplateView):
    """The Main for to buy Page"""
    template_name = 'to_buy_home.html'

    def queryset(self):
        query = models.ListToBuy.objects.filter(enabled=True)
        query = query.annotate(
            count=Count(
                'itemlisttobuy',
                filter=Q(itemlisttobuy__enabled=True)
            )
        )
        return query

    def my_list_queryset(self, pk: int):
        query = self.queryset()
        return query.filter(created_by=pk)

    def shared_queryset(self, pk: int):
        query = self.queryset()
        return query.filter(users__id__in=[pk])

    def paginate(self, data: list):
        return Paginator(data, settings.PAGINATION_LIMIT)

    def get(self, request):
        my_lists = self.paginate(self.my_list_queryset(self.request.user))
        count_my_lists = my_lists.count
        my_lists = my_lists.page(request.GET.get("page_my_list") or 1)
        shared_lists = self.paginate(self.shared_queryset(self.request.user.pk))
        count_shared_lists = shared_lists.count
        shared_lists = shared_lists.page(request.GET.get("page_shared_list") or 1)

        args = {
            "my_lists": my_lists.object_list,
            "my_lists_paginator": my_lists,
            "count_my_lists": count_my_lists,

            "shared_lists": shared_lists.object_list,
            "shared_lists_paginator": shared_lists,
            "count_shared_lists": count_shared_lists,
        }
        return render(request, self.template_name, args)


class ToBuyNewView(generic.edit.FormView):
    template_name = 'to_buy/edit.html'
    form_class = forms.ListToBuyForm
    success_url = 'to_buy:home_buys'

    def get_form_kwargs(self):
        kwargs = super(ToBuyNewView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.pk
        return kwargs

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(ToBuyNewView, self).get_context_data(**kwargs)
        context['mode'] = 'Save'
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{"user": self.request.user},
        )
        self.object.save()
        self.object.users.set([x.pk for x in form.cleaned_data["users"]])
        self.object.save()
        return redirect(self.get_success_url())


class DetailToBuyView(LoginRequiredMixin, generic.detail.DetailView):
    """Detail Board View"""
    model = models.ListToBuy
    template_name = 'to_buy/detail.html'

    def queryset_list(self, pk):
        return models.ItemListToBuy.objects.filter(enabled=True, list=pk)

    def queryset_products(self, pk, query = None):
        my_list = [x.product.pk for x in self.queryset_list(pk)]
        data = (
            product_models.Product.objects.filter(
                enabled=True,
            )
            .exclude(pk__in=my_list)
        )
        if query:
            data = data.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return data

    def paginate(self, data: list):
        return Paginator(data, settings.PAGINATION_LIMIT)

    def get_context_data(self, *args, **kwargs):
        """Context generated by detail board"""
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q") or None

        products = self.paginate(self.queryset_products(context['listtobuy'], query))
        count_products = products.count
        products = products.page(self.request.GET.get("page_products") or 1)

        items = self.paginate(self.queryset_list(context['listtobuy']))
        count_items = items.count
        items = items.page(self.request.GET.get("page_items") or 1)

        context['items'] = items
        context['products'] = products
        context["count_products"] = count_products
        context["count_items"] = count_items
        context["search"] = query
        return context


class ToBuyNewItemView(LoginRequiredMixin, generic.edit.FormView):
    model = models.ItemListToBuy
    template_name = "to_buy/item/edit.html"
    form_class = forms.ItemListToBuyForm
    success_url = 'to_buy:buys_add_product'
    mode = "Save"

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{"user": self.request.user},
        )
        self.object.save()
        return redirect(self.get_success_url(), pk=self.kwargs["pk"])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["mode"] = self.mode
        context["form"] = forms.ItemListToBuyForm(
            list_id=self.kwargs["pk"],
            product_id=self.kwargs["pk_item"]
        )
        context["list_id"] = self.kwargs["pk"]
        context["product_id"] = self.kwargs["pk_item"]
        context["product"] = product_models.Product.objects.filter(
            pk=self.kwargs["pk_item"]
        ).first()
        return context


class ToBuyEditItemView(LoginRequiredMixin, generic.edit.UpdateView):
    model = models.ItemListToBuy
    template_name = "to_buy/item/edit.html"
    form_class = forms.ItemListToBuyForm
    success_url = 'to_buy:buys_add_product'
    mode = "Edit"

    def get_object(self):
        return self.model.objects.filter(
            product__pk=self.kwargs["pk_item"],
            list__pk=self.kwargs["pk"],
            enabled=True,
        ).first()

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{"user": self.request.user},
        )
        self.object.save()
        return redirect(self.get_success_url(), pk=self.kwargs["pk"])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["mode"] = self.mode
        context["form"] = forms.ItemListToBuyForm(
            list_id=self.kwargs["pk"],
            product_id=self.kwargs["pk_item"],
            instance=self.get_object()
        )
        context["list_id"] = self.kwargs["pk"]
        context["product_id"] = self.kwargs["pk_item"]
        context["product"] = product_models.Product.objects.filter(
            pk=self.kwargs["pk_item"]
        ).first()
        return context



def delete_list_to_but(request, pk):
    model = models.ListToBuy
    list = get_object_or_404(model, pk=pk)
    list.enabled = False
    list.save()
    return redirect("to_buy:home_buys")


def add_product_to_list(request, pk):
    form = forms.ItemListToBuyCompleteForm(request.POST)
    if form.is_valid:
        object = form.save(
            commit=False,
            **{"user": request.user},
        )
        object.save()
    return redirect("to_buy:buys_show", pk=pk)


def edit_product_to_list(request, pk, pk_item):
    model = models.ItemListToBuy
    item = get_object_or_404(model, pk=pk_item)
    item.quantity = request.POST.get("quantity")
    item.save()
    return redirect("to_buy:buys_show", pk=pk)


def delete_product_to_list(request, pk, pk_item):
    model = models.ItemListToBuy
    item = get_object_or_404(model, pk=pk_item)
    item.enabled = False
    item.save()
    return redirect("to_buy:buys_show", pk=pk)


def convert_item(data):
    return """
    name: {}
    description: {}
    quantity: {}
    """.format(data.product.name, data.product.description, data.quantity)


def convert_list_to_message(dataquery) -> str:
    data = list(map(convert_item, dataquery))
    return """
    List to Buy
    ----
    {}
    ----
    """.format("---\n".join(data))

def telegram_send_list(request, pk):
    items = models.ItemListToBuy.objects.filter(enabled=True, list=pk)
    telegram.send_message(convert_list_to_message(items), "+573125086310")
    return redirect("to_buy:buys_show", pk=pk)
