from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^cal/', include('calligraphy.urls')),
    url(r'^admin/', admin.site.urls),
]
