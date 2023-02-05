from dal import autocomplete
from . import models

class AuthorAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return models.Authors.objects.none()

        qs = models.Authors.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs