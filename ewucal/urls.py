from django.conf.urls import url, include
from django.contrib import admin
import socket

urlpatterns = []
if socket.gethostname() == 'bigArch':
    urlpatterns.append(url(r'^home/dave/workspace/pycharm/media/', include('calligraphy.urls')))
else:
    urlpatterns.append(url(r'^media/', include('calligraphy.urls')))

urlpatterns.append(url(r'^admin/', admin.site.urls))
