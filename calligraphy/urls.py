#
# ├── chars
# │   ├── 06100004
# │   │   ├── 00000009(266,179,402,296).jpg (0-1243,2-1840,21-1326,45-1938)
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
    url(r'^pages/[0-9]{8}-[0-9]{8}.(?:jpg|png|tif)$', views.page_i)
]
