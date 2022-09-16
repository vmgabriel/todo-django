"""All Views of cash flow"""

# Libraries
import calendar
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Case, When, FloatField
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import ExtractDay, Abs
from django.utils.timezone import make_aware

# Modules
from django.conf import settings
from djmoney.money import Money

from accounts.models import User
from . import models, forms


def get_days_month(
        month: int = datetime.now().month,
        year: int = datetime.now().year
) -> int:
    return calendar.monthrange(year, month)[1] + 1


def get_start_and_end_date_from_calendar_week(
        year: int,
        calendar_week: int
) -> list[datetime]:
    monday = datetime.strptime(f'{year}-{calendar_week}-1', "%Y-%W-%w")
    monday = make_aware(monday)
    return  [monday] + [monday + timedelta(days=x) for x in range(1,7)]

class CashFlowHomeView(generic.TemplateView):
    """The Main for to Cash Flow"""
    template_name = 'cash_flow_home.html'

    def queryset(self):
        query = models.FlowMoney.objects.filter(
            enabled=True,
            created_by=self.request.user.pk
        )
        return query

    def queryset_per_day(self, day: datetime.date) -> list[models.FlowMoney]:
        query = self.queryset()
        return query.filter(date_flow__date=day)

    def queryset_sum_per_month_category(
            self,
            year: int = datetime.now().year,
            month: int = datetime.now().month,
    ):
        day = datetime.now().day
        query = self.queryset().filter(
            date_flow__year=year,
            date_flow__month=month,
            category__parent_category__type_flow__in=models.TypeFlow.EXPENDITURE,
        ).annotate(
            main_category=F("category__parent_category__name")
        ).values("main_category").annotate(
            day=ExtractDay("date_flow"),
        ).values("day", "main_category").annotate(
            total=Sum(Abs("amount")),
        ).values("day", "total", "main_category")
        categories = {}
        for x in query:
            if x["main_category"] in categories:
                categories[x["main_category"]][x["day"]] = float(x["total"])
            else:
                categories[x["main_category"]] = {x["day"]: float(x["total"])}
        for counted in range(1, day):
            for x in categories.values():
                if counted not in x:
                    x[counted] = 0
        return {k: sorted(x.items(), key=lambda x: x[0]) for k, x in categories.items()}

    def queryset_sum_per_month(
            self,
            year: int = datetime.now().year,
            month: int = datetime.now().month
    ) -> list:
        day = datetime.now().day
        query = self.queryset().filter(
            date_flow__year=year,
            date_flow__month=month,
        ).annotate(
            day=ExtractDay("date_flow"),
        ).values("day").annotate(
            total=Sum("amount"),
        ).values("day", "total")
        previous_val = 0
        definition = {}
        for x in query:
            definition[x["day"]] = previous_val + float(x["total"])
            previous_val += float(x["total"])
        previous_val = 0
        for counted in range(1, day):
            if counted not in definition:
                definition[counted] = previous_val
            else:
                previous_val = definition[counted]
        return sorted(definition.items(), key=lambda x: x[0])

    def queryset_sum_per_day_week(
            self,
            week: int,
            year: int = datetime.now().year,
            month: int = datetime.now().month,
    ):
        days_in_week = get_start_and_end_date_from_calendar_week(year, week)
        query = self.queryset().filter(
            date_flow__year=year,
            date_flow__month=month,
            date_flow__gt=days_in_week[0],
            date_flow__lt=days_in_week[-1],
        ).annotate(
            day=ExtractDay("date_flow"),
        ).values("day").annotate(
            total_positive=Sum(Case(When(amount__gt=0, then=F("amount")), default=0, output_field=FloatField())),
            total_negative=Sum(Case(When(amount__lt=0, then=Abs(F("amount"))), default=0, output_field=FloatField())),
        ).values("day", "total_positive", "total_negative")
        definition = {x["day"]: {"positive": float(x["total_positive"]), "negative": float(x["total_negative"])} for x in query}
        ordered = []
        for day in days_in_week:
            if day.day not in definition:
                definition[day.day] = {"positive": 0, "negative": 0}
        for day in days_in_week:
            ordered.append(definition[day.day])
        return ordered


    def order_by_levels(self, l: list) -> list:
        completed = []
        m = max([x.count() for x in l])
        for x in range(m):
            the_list = []
            for y in l:
                try:
                    the_list.append(y[x])
                except IndexError:
                    the_list.append(None)
            completed.append(the_list)
        return completed

    def get(self, request):
        dt = datetime.now()
        week_in_year = dt.isocalendar().week
        week = get_start_and_end_date_from_calendar_week(dt.year, week_in_year)
        money_flow_week = self.order_by_levels([self.queryset_per_day(day) for day in week])
        spend_by_month = {
            "Spend": {
                "data": [x for _, x in self.queryset_sum_per_month(dt.year, dt.month)],
                "color": "04aa6d",
            }
        }
        by_categories = {
            k: {
                "data": [x[1] for x in vals],
                "color": models.CategoryFlow.objects.filter(name=k).first().color,
            }
            for k,vals in self.queryset_sum_per_month_category(dt.year,dt.month).items()
        }

        # DataSource object
        args = {
            # Personal User
            "wallet": self.request.user.wallet or Money(0, "COP"),
            "alkali": self.request.user.alkali or Money(0, "COP"),
            "labels": list(range(1,get_days_month())),

            "by_categories": by_categories,
            "spend_by_month": spend_by_month,
            "week": week,
            "money_flow_week": money_flow_week,
            "total_per_week": self.queryset_sum_per_day_week(week_in_year),
        }
        return render(request, self.template_name, args)


class FlowMoneyNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = 'flow_money/edit.html'
    form_class = forms.FlowMoneyForm
    success_url = "cash_flow:home_cash_flow"

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(FlowMoneyNewView, self).get_context_data(**kwargs)
        context['mode'] = 'Save'
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{'user': self.request.user}
        )
        self.object.save()

        # Verify if these is increase o decrese
        type_flow = self.object.category.type_flow
        amount = self.object.amount
        if type_flow == models.TypeFlow.INCOME:
            # Increase
            if self.object.category.parent_category.name.lower() == "saving":
                self.request.user.add_to_alkali(amount)
        self.request.user.add_to_wallet(amount)
        self.request.user.save()

        return redirect(self.get_success_url())


class FlowMoneyEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = models.FlowMoney
    form_class = forms.FlowMoneyForm
    template_name = "flow_money/edit.html"
    success_url = "cash_flow:home_cash_flow"

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(FlowMoneyEditView, self).get_context_data(**kwargs)
        context['mode'] = 'Update'
        return context

    def form_valid(self, form):
        """Get Form Valid"""
        self.object = form.save(commit=False, updated=True)
        self.object.save()

        # Verify if these is increase o decrese
        type_flow = self.object.category.type_flow
        amount = self.object.amount
        if type_flow == models.TypeFlow.INCOME:
            # Increase
            if self.object.category.parent_category.name.lower() == "saving":
                self.request.user.add_to_alkali(amount)
        self.request.user.add_to_wallet(amount)
        self.request.user.save()

        return redirect(self.get_success_url())


class CategoryFlowListView(LoginRequiredMixin, generic.list.ListView):
    model = models.CategoryFlow
    paginate_by = settings.PAGINATION_LIMIT
    context_object_name = 'categories_flow'
    template_name = 'categories_flow/index.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super(CategoryFlowListView, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(enabled=True, parent_category__isnull=False)
        return queryset

    def get_queryset_primary(self, *args, **kwargs):
        queryset = super(CategoryFlowListView, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(parent_category__isnull=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryFlowListView, self).get_context_data(*args, **kwargs)
        context['count'] = self.get_queryset().count()
        context["primary"] = self.get_queryset_primary()
        context["count_primary"] = context["primary"].count()

        return context


class CategoryFlowNewView(LoginRequiredMixin, generic.edit.FormView):
    template_name = 'categories_flow/edit.html'
    form_class = forms.CategoryFlowForm
    success_url = "cash_flow:categories"

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(CategoryFlowNewView, self).get_context_data(**kwargs)
        context['mode'] = 'Save'
        return context

    def form_valid(self, form):
        self.object = form.save(
            commit=False,
            **{'user': self.request.user}
        )
        self.object.save()
        return redirect(self.get_success_url())


class CategoryFlowEditView(LoginRequiredMixin, generic.edit.UpdateView):
    model = models.CategoryFlow
    form_class = forms.CategoryFlowForm
    template_name = "categories_flow/edit.html"
    success_url = "cash_flow:categories"

    def get_context_data(self, **kwargs):
        """Get Context Data"""
        context = super(CategoryFlowEditView, self).get_context_data(**kwargs)
        context['mode'] = 'Update'
        return context

    def form_valid(self, form):
        """Get Form Valid"""
        self.object = form.save(commit=False, updated=True)
        self.object.save()
        return redirect(self.get_success_url())


@login_required
def delete_category(request, pk):
    model = models.CategoryFlow
    category = get_object_or_404(model, pk=pk)
    category.enabled = False
    category.save()
    return redirect("cash_flow:categories")