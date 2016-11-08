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
    url(r'^page/(?P<page_id>[0-9]+)$',  views.individual_page),
    url(r'^validate',                   views.validate_html),
    url(r'^ajax/get_page',              views.get_page),
    url(r'^ajax/get_char_relatives',    views.get_char_relatives),
    url(r'^ajax/get_root_tree',         views.get_root_tree),
    url(r'^ajax/validate',              views.validate_ajax),
    url(r'^$',                          views.webroot)
]
