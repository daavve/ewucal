#
# ├── chars
# │   ├── 06100004
# │   │   ├── 00000009(266,179,402,296).jpg (#-####) for each coordinate
# ├── pages
# │   ├── 06100004-00000009.(png,jpg,tif)
# ├── scanned
# │   └── 1
# │       ├── 10i.png
# │       ├── 10t.png
# │       ├── 4i.png
#
############################################
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^auth/(?P<auth_id>[0-9]+)$', views.auth_works),
    url(r'^pages/[0-9]{8}-[0-9]{8}\.(?:jpg|png|tif)$', views.page_i),
    url(r'^scanned/[0-9]{1,2}/[0-9]{1,2}i\.png', views.page_i),
    url(r'^chars/[0-9]{8}/[0-9]{8}\([0-9]{1,4},[0-9]{1,4},[0-9]{2,4},[0-9]{2,4}\)\.jpg$', views.char_i),
    url(r'^$', views.auth_list)
]
