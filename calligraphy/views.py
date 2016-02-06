#
# Logic of application goes here:  Receive Request -> Process -> Serve Response
#
###################################################

from django.http import HttpResponse


def index(request):
    return HttpResponse("Calligraphy App.")
