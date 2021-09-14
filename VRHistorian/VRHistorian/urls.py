# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.views.generic import TemplateView
from VRHistorian.views import upload, upload_multi, pano, download, clear_olds, view_imgs_all

import spirit.urls

# Override admin login for security purposes
from django.contrib.auth.decorators import login_required

admin.site.login = login_required(admin.site.login)

urlpatterns = [
    url(r'^', include(spirit.urls)),


    url(r'^static/', download),
    # This is the default django admin
    # it's not needed to use Spirit
    url(r'^admin/', admin.site.urls),
    url(r'^view_imgs_all/', view_imgs_all),
    url(r'^upload/', upload),
    url(r'^upload_multi/', upload_multi),
    url(r'^clear_olds/', clear_olds),
    url(r'^pano/', pano),
    url(r'^download/', download),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
