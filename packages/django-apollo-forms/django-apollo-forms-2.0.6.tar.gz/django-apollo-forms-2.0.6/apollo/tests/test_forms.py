from django.test import TestCase
from django.core.exceptions import ValidationError
from django import forms
from apollo.models import FormFieldTemplate
from apollo.forms import SubmissionForm
from apollo.factories import FormFactory, FormFieldFactory, FormFieldTemplateFactory, FormSubmissionFactory
import mock
import pdb


class TestSubmissionForm(TestCase):
    def setUp(self):
        self.form = FormFactory.create()

        self.field_name = FormFieldFactory(
            form=self.form,
            default_value='Bob',
            validation_rule=FormFieldTemplate.RULE_REQUIRED,
            template=FormFieldTemplateFactory(name='name')
        )
        self.field_email = FormFieldFactory(
            form=self.form,
            validation_rule=FormFieldTemplate.RULE_EMAIL,
            template=FormFieldTemplateFactory(name='email')
        )
        self.field_phone = FormFieldFactory(
            form=self.form,
            validation_rule=FormFieldTemplate.RULE_OPTIONAL,
            template=FormFieldTemplateFactory(name='phone')
        )

    def _get_sform(self, fields_data, clean_data=True):
        sform = SubmissionForm(apollo_fields=[self.field_name, self.field_email, self.field_phone], data=fields_data)
        return sform

    def test_valid_data_validates(self):
        sform = self._get_sform({
            'name': 'Bobby',
            'email': 'bobby@test.com'
        })

        self.assertTrue(sform.is_valid())

        sform = self._get_sform({
            'name': 'Test',
            'email': 'bobby@test.com',
        })

        self.assertTrue(sform.is_valid())

    def test_invalid_data_doesnt_validate(self):
        sform = self._get_sform({
            'email': 'bobby@test.com'
        })

        self.assertFalse(sform.is_valid())

        sform = self._get_sform({
            'name': 'bobby',
            'email': 'bobby@'
        })

        self.assertFalse(sform.is_valid())

    def test_cleaned_data_is_correct(self):
        sform = self._get_sform({
            'name': 'Test',
            'email': 'bobby@test.com',
        })

        sform.is_valid()

        self.assertDictEqual(
            sform.cleaned_data,
            {
                'name': 'Test',
                'email': 'bobby@test.com',
                'phone': ''
            }
        )

    def test_get_widget_for_apollo_field(self):
        form = SubmissionForm()

        # text field should return text widget
        widget = form.get_widget_for_apollo_field(
            FormFieldFactory(
                form=self.form,
                template=FormFieldTemplateFactory(name='test1', input_type='TEXT')
            )
        )

        self.assertEqual(widget.input_type, 'text')

        # hidden field should return hidden widget
        widget = form.get_widget_for_apollo_field(
            FormFieldFactory(
                form=self.form,
                template=FormFieldTemplateFactory(name='test2', input_type='HIDDEN')
            )
        )

        self.assertEqual(widget, forms.HiddenInput)

        # textarea field should return textarea widget
        widget = form.get_widget_for_apollo_field(
            FormFieldFactory(
                form=self.form,
                template=FormFieldTemplateFactory(name='test3', input_type='TEXTAREA')
            )
        )

        self.assertEqual(widget, forms.Textarea)

        # select field should return select widget
        widget = form.get_widget_for_apollo_field(
            FormFieldFactory(
                form=self.form,
                template=FormFieldTemplateFactory(name='test4', input_type='SELECT')
            )
        )

        self.assertEqual(widget, forms.Select)

        # checkbox field should return checkbox widget
        widget = form.get_widget_for_apollo_field(
            FormFieldFactory(
                form=self.form,
                template=FormFieldTemplateFactory(name='test5', input_type='CHECKBOX')
            )
        )

        self.assertEqual(widget, forms.CheckboxInput)

        # richtext field should return no widget
        widget = form.get_widget_for_apollo_field(
            FormFieldFactory(
                form=self.form,
                template=FormFieldTemplateFactory(name='test6', input_type='RICHTEXT')
            )
        )

        self.assertIsNone(widget)

    def test_get_widget_attrs_for_apollo_field(self):
        form = SubmissionForm()

        attrs = form.get_widget_attrs_for_apollo_field(
            FormFieldFactory(
                form=self.form,
                placeholder=None,
                template=FormFieldTemplateFactory(name='test1')
            )
        )

        self.assertDictEqual(attrs, {})

        attrs = form.get_widget_attrs_for_apollo_field(
            FormFieldFactory(
                form=self.form,
                placeholder='foobar',
                template=FormFieldTemplateFactory(name='test2')
            )
        )

        self.assertDictEqual(attrs, {'placeholder': 'foobar'})