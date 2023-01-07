"""All Forms of Cash Flow"""

# Libraries
from django import forms
from djmoney.money import Money

# Modules
from . import models


class CategoryFlowForm(forms.ModelForm):
    """Category Flow Form Control"""

    def __init__(self, *args, **kwargs):
        super(CategoryFlowForm, self).__init__(*args, **kwargs)
        self.fields["parent_category"].queryset = models.CategoryFlow.objects.filter(
            parent_category=None
        )

    class Meta:
        """Meta Category Form"""
        model = models.CategoryFlow
        fields = [
            "name",
            "description",
            "color",
            "parent_category",
            "state_flow",
            "type_flow",
        ]

    def save(self, commit=True, updated=False, **kwargs):
        """Save of Category flow with the form"""
        obj = super(CategoryFlowForm, self).save(commit=False)

        if not updated:
            obj.created_by = kwargs.get('user')
        obj.updated_by = kwargs.get('user')

        if commit:
            obj.save()
        return obj


class FlowMoneyForm(forms.ModelForm):
    """Flow Money Form Control"""

    def __init__(self, *args, **kwargs):
        if "instance" in kwargs:
            kwargs["instance"].amount = abs(kwargs["instance"].amount)
        super(FlowMoneyForm, self).__init__(*args, **kwargs)
        self.fields["category"].queryset = models.CategoryFlow.objects.exclude(
            parent_category=None
        )

    class Meta:
        """Meta Category Form"""
        model = models.FlowMoney
        fields = [
            "description",
            "category",
            "amount",
            "date_flow",
        ]

    def save(self, commit=True, updated=False, **kwargs):
        obj = super(FlowMoneyForm, self).save(commit=False)

        type_flow = obj.category.type_flow
        if obj.amount < Money(0, "COP"):
            obj.amount = abs(obj.amount)
        if type_flow != models.TypeFlow.INCOME:
            # this is for exit of money
            obj.amount = -obj.amount

        if not updated:
            obj.created_by = kwargs.get('user')
        obj.updated_by = kwargs.get('user')

        if commit:
            obj.save()
        return obj