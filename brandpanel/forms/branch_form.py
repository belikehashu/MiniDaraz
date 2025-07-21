from django import forms
from brandpanel.models.branch import Branch

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name']
