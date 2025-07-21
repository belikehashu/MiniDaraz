from django import forms
from managerpanel.models.manager import Manager

class AssignManagerForm(forms.Form):
    manager = forms.ModelChoiceField(queryset=Manager.objects.none())

    def __init__(self, *args, **kwargs):
        branch = kwargs.pop('branch', None)
        super().__init__(*args, **kwargs)
        if branch:
            brand_managers = Manager.objects.filter(user__role='manager', branches__brand=branch.brand).distinct()
            self.fields['manager'].queryset = brand_managers
