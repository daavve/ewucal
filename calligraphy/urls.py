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
    url(r'^validate/eval-bad-pages',                                views.eval_bad_pages),
    url(r'^validate/draw-chars/(?P<old_or_new>[0-9]+)$',            views.draw_chars),
    url(r'^validate/compare-chars',                                 views.compare_chars),
    url(r'^validate/examine-predictions',                           views.examine_predictions),
    url(r'^validate',                                               views.validate_root),
    url(r'^ajax/get_progress',                                      views.get_progress),
    url(r'^ajax/get_page',                                          views.get_page),
    url(r'^ajax/get_char_relatives',                                views.get_char_relatives),
    url(r'^ajax/get_root_tree',                                     views.get_root_tree),
    url(r'^ajax/get_features',                                      views.get_features),
    url(r'^ajax/validate',                                          views.validate_ajax),
    url(r'^ajax/get_to_verify_page',                                views.get_to_verify_page),
    url(r'^ajax/find_boxes',                                        views.find_boxes),
    url(r'^ajax/get_bad_pages',                                     views.get_bad_pages),
    url(r'^ajax/post_offsets',                                      views.post_offsets),
    url(r'^ajax/post_characters',                                   views.post_characters),
    url(r'^$',                                                      views.webroot)
]
