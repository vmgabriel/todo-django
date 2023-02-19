from django import forms


class MaterializeFileInput(forms.ClearableFileInput):
    template_name = "fields/file.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        print("context - ", context)
        return context
