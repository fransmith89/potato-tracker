from django import forms
from django.contrib.auth import get_user_model

from crispy_forms_foundation.forms import FoundationModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Project, Ticket


class BaseTrackerForm(FoundationModelForm):
    def __init__(self, user=None, title=None, *args, **kwargs):
        self.title = title
        self.user = user

        super(BaseTrackerForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

    def save(self, *args, **kwargs):
        commit = kwargs.pop('commit', True)
        instance = super(BaseTrackerForm, self).save(
            commit=False, *args, **kwargs)

        self.pre_save(instance)

        if commit:
            instance.save()

        return instance

    def pre_save(self, instance):
        pass


class ProjectForm(BaseTrackerForm):
    class Meta:
        model = Project
        fields = ('title',)

    def pre_save(self, instance):
        instance.created_by = self.user


class TicketForm(BaseTrackerForm):
    assignees = forms.ModelMultipleChoiceField(queryset=None, required=False)

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'assignees',)

    def __init__(self, project=None, *args, **kwargs):
        self.project = project
        super(TicketForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_error_title = 'The following errors occurred:'
        self.helper.add_input(Submit('submit', 'Submit', css_class='submit button'))
        self.fields['assignees'].queryset = get_user_model().objects.all()

    def pre_save(self, instance):
        instance.created_by = self.user
        instance.project = self.project

    def clean(self):
        if self.instance.pk and self.project.id != self.instance.project_id:
            err_msg = (
                'The ticket\'s current project id is not the same as the project id provided '
                'in the URL. Return to the project\'s page and select the ticket again.'
            )
            self.add_error(None, err_msg)
        return self.cleaned_data
