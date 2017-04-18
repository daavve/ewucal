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
    url(r'^page/(?P<page_id>[0-9]+)$',                              views.individual_page),
    url(r'^validate/view-progress',                                 views.view_progress),
    url(r'^validate/find-offsets',                                  views.validate_find_offsets),
    url(r'^validate/draw-chars/(?P<old_or_new>[0-9]+)$',            views.draw_chars),
    url(r'^validate',                                               views.validate_root),
    url(r'^ajax/get_progress',                                      views.get_progress),
    url(r'^ajax/get_page',                                          views.get_page),
    url(r'^ajax/get_char_relatives',                                views.get_char_relatives),
    url(r'^ajax/get_root_tree',                                     views.get_root_tree),
    url(r'^ajax/validate',                                          views.validate_ajax),
    url(r'^ajax/get_to_verify_page',                                views.get_to_verify_page),
    url(r'^ajax/get_toshi',                                         views.get_toshi),
    url(r'^ajax/post_offsets',                                      views.post_offsets),
    url(r'^ajax/post_characters',                                   views.post_characters),
    url(r'^$',                                                      views.webroot)
]
