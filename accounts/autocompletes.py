from dal import autocomplete
from . import models

class UserAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return models.User.objects.none()

        qs = models.User.objects.all()

        if self.q:
            qs = qs.filter(accounts__icontains=self.q)

        return qs