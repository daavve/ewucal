from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = []

urlpatterns.append(url(r'^admin/', admin.site.urls))
urlpatterns.append(url(r'^', include('calligraphy.urls')))
