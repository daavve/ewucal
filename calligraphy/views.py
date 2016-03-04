#
# Logic of application goes here:  Receive Request -> Process -> Serve Response
#
###################################################

from django.http import HttpResponse
from django.template import Context, loader
from .models import Author


def auth_list(request):
    authors = Author.objects.all()
    tmplt = loader.get_template('calligraphy/authors.html')
    cntxt = Context({'authors': authors})
    return HttpResponse(tmplt.render(cntxt))

def auth_works(request):
    return HttpResponse(str(request))



def page_i(request):
    return HttpResponse("Image Request")


def char_i(request):
    return HttpResponse("Character Request")

