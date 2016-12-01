from django.conf.urls import url, include

urlpatterns = [
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^', include('calligraphy.urls'))
]
