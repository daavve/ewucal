#
# Logic of application goes here:  Receive Request -> Process -> Serve Response
#
###################################################

from django.http import HttpResponse


def page_i(request):
    return HttpResponse("Page Request")

