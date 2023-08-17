from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .settings import apollo_settings
import django.dispatch
import logging

logger = logging.getLogger(__name__)


#####-----< Triggers >----#####
# fired when a form is submitted to the backend, but before the submission is cleaned / validated
# provides: raw_data, form_id
form_submitted = django.dispatch.Signal()

# fired after a form submission is cleaned / validated
# provides: cleaned_data, form_id, submission_id
form_submission_cleaned = django.dispatch.Signal()

# fired on a form submission error
# provides: error, raw_data, form_id
form_submission_error = django.dispatch.Signal()

# fired to signal a webhook to trigger
# provides: hook, data
external_webhook_triggered = django.dispatch.Signal()

# fired on a external webhook error
# provides: error, url, data
external_webhook_error = django.dispatch.Signal()


#####-----< Listeners >----#####
@receiver(post_save)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    from .models import APIUser

    if created and sender is APIUser:
        logger.debug('creating auth token for new API user')
        Token.objects.create(user=instance.auth_user)


@receiver(form_submission_cleaned)
def fire_form_submission_webhooks(sender, cleaned_data=None, form_id=None, submission_id=None, **kwargs):
    # import here to avoid circular deps
    from .models import Form, FormSubmission, ExternalWebhook
    from .api import serializers

    form = Form.objects.get(id=form_id)
    webhooks = form.external_hooks.filter(for_event=ExternalWebhook.EVENT_SUBMISSION_CREATED)

    if webhooks.exists():
        for hook in webhooks:
            data = serializers.FormSubmissionSerializer(instance=FormSubmission.objects.get(id=submission_id)).data

            external_webhook_triggered.send(sender, hook=hook, data=data)

            if not apollo_settings.EXTERNAL_HOOKS_SIGNAL_ONLY:
                logger.debug('sending submission data to hook %s' % hook)
                hook.send_data(data)
