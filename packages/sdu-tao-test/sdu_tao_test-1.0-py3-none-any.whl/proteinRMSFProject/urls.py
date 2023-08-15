from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from homeApp.views import home
from homeApp.views import submit_form_view
from homeApp.views import rmsf
from homeApp.views import batch
from homeApp.views import moleccular
from homeApp.views import help
from homeApp.views import mail

urlpatterns = [
    path('admin/', admin.site.urls),  # 管理员
    path('', home, name='home'),  # 首页
    path('submit_form_view', submit_form_view, name='submit_form_view'),  # 首页
    path('mail', mail, name='mail'),  # 首页
    path('rmsf/', rmsf, name='rmsf'),  # RMSF prediction
    path('batch/', batch, name='batch'),  # batch prediction
    path('moleccular/', moleccular, name='moleccular'),  # Moleccular Dynamics Simulation Database
    path('help/', help, name='help'),  # help
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
