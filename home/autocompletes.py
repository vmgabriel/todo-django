from dal import autocomplete
from . import models


class HomeAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return models.Home.objects.none()

        qs = models.Home.objects.all()

        if self.q:
            qs = qs.filter(direction__icontains=self.q)

        return qs


class DepartmentHomeAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return models.DepartmentHome.objects.none()

        qs = models.DepartmentHome.objects.all()

        if self.q:
            qs = qs.filter(code__icontains=self.q)

        return qs