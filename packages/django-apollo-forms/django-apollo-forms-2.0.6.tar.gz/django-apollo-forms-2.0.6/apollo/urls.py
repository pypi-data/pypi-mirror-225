from django.views.decorators.clickjacking import xframe_options_exempt
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from .settings import apollo_settings
from .views import FormManager, DownloadFormSubmissions, NoScriptForm
from .api import urls as api_urls
import os


form_builder_view = FormManager.as_view()
if apollo_settings.BUILDER_REQUIRES_IS_STAFF:
    form_builder_view = staff_member_required(form_builder_view)

download_submissions_view = DownloadFormSubmissions.as_view()
if apollo_settings.DOWNLOAD_REQUIRES_IS_STAFF:
    download_submissions_view = staff_member_required(download_submissions_view)

urlpatterns = [
    re_path('builder/(.*/)?', form_builder_view),
    path('download/', download_submissions_view),
    path('render/', xframe_options_exempt(NoScriptForm.as_view()), name='render_noscript'),
    path('%s/' % os.path.join(apollo_settings.API_ROOT, apollo_settings.API_VERSION), include(api_urls))
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()