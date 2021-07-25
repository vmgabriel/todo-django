"""Form Todos"""

# Libraries
from django.forms import ModelForm

# Models
from .models import Card, Board


class BoardForm(ModelForm):
    """Board Form Control for Generate Model"""
    class Meta:
        """Meta Board Form"""
        model = Board
        fields = [
            'title'
        ]

    def save(self, commit=True, **kwargs):
        """Save of Board with the form"""
        obj = super(BoardForm, self).save(commit=False)
        obj.creator_ref = kwargs.get('user')

        if commit:
            obj.save()
        return obj


class CardForm(ModelForm):
    """Card Form Control for Generate Model"""
    class Meta:
        """Meta Card Form"""
        model = Card
        fields = [
            'title',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["class"] = "materialize-textarea"

    def save(self, commit=True, **kwargs):
        """Save of Card with the form"""
        obj = super(CardForm, self).save(commit=False)
        obj.board_ref = Board.objects.get(id=kwargs.get('board'))

        if commit:
            obj.save()
        return obj
