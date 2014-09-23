from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.models import modelformset_factory, BaseModelFormSet
from .models import Website, Section


class AddWebsiteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddWebsiteForm, self).__init__(*args, **kwargs)
        self.fields['unique_users_per_day'].widget = forms.TextInput()
        self.fields['page_views_per_day'].widget = forms.TextInput()
        self.fields['unique_users_per_month'].widget = forms.TextInput()
        self.fields['page_views_per_month'].widget = forms.TextInput()
        self.fields['vertical_category'].empty_label = "Vertical Category"

    class Meta:
        model = Website
        exclude = ['user',]

class AddSectionForm(forms.Form):
    url = forms.URLField()
    section_name = forms.CharField(max_length=100)


class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

AddSectionFormSet = formset_factory(AddSectionForm, formset=RequiredFormSet)
