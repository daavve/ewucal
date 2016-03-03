#
# Logic of application goes here:  Receive Request -> Process -> Serve Response
#
###################################################

from django.http import HttpResponse


def page_i(request):
    return HttpResponse("Image Request")

def char_i(request):
    return HttpResponse("Character Request")

