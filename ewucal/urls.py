from django.conf.urls import url, include
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^accounts/profile/$', RedirectView.as_view(url='/', permanent=False)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^', include('calligraphy.urls'))
]
