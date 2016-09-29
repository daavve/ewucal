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
    url(r'^auth/(?P<auth_id>[0-9]+)$',  views.works_by_author),
    url(r'^work/(?P<work_id>[0-9]+)$',  views.pages_in_work),
    url(r'^page/(?P<page_id>[0-9]+)$',  views.individual_page),
    url(r'^char/(?P<char_id>[0-9]+)$',  views.individual_char),
    url(r'^ajax/get_page',             views.get_page),
    url(r'^ajax/get_page_chars',       views.get_page_chars),
    url(r'^ajax/get_char_relatives',   views.get_char_relatives),
    url(r'^$', views.auth_list)
]
