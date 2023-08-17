from django import forms


class SubmissionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # apollo fields are the Apollo FormField objects defined in an Apollo Form object
        apollo_fields = kwargs.pop('apollo_fields', [])
        super(SubmissionForm, self).__init__(*args, **kwargs)

        for f in apollo_fields:
            field_kwargs = dict(
                required=f.is_required,
                label=f.label,
                initial=f.default_value
            )

            widget = self.get_widget_for_apollo_field(f)
            if widget:
                field_kwargs['widget'] = widget(attrs=self.get_widget_attrs_for_apollo_field(f))

            if f.validation_rule == 'EMAIL':
                self.fields[f.name] = forms.EmailField(**field_kwargs)
            else:
                self.fields[f.name] = forms.CharField(**field_kwargs)

    def get_widget_for_apollo_field(self, af):
        widget_map = {
            'TEXT': forms.TextInput,
            'TEXTAREA': forms.Textarea,
            'SELECT': forms.Select,
            'CHECKBOX': forms.CheckboxInput,
            'RADIO': forms.RadioSelect
        }

        # hidden is a bit of a special case, since the field may be hidden as a result of being input type = Hiddden OR
        # by virtue of having it's is_visible field = False
        try:
            return forms.HiddenInput if not af.is_visible else widget_map[af.input_type]
        except KeyError:
            return None

    def get_widget_attrs_for_apollo_field(self, af):
        attrs = {}

        if af.placeholder:
            attrs['placeholder'] = af.placeholder

        return attrs
