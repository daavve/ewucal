#
# Logic of application goes here:  Receive Request -> Process -> Serve Response
#
###################################################

from django.http import HttpResponse
from django.template import loader
from .models import Author, Work, Page, Character


def auth_list(request):
    authors = Author.objects.all()
    tmplt = loader.get_template('calligraphy/authors.html')
    cntxt = {'authors': authors}
    return HttpResponse(tmplt.render(context=cntxt, request=request))


def works_by_author(request, auth_id):
    works = Work.objects.filter(author=auth_id)
    tmplt = loader.get_template('calligraphy/works.html')
    cntxt = {'works': works}
    return HttpResponse(tmplt.render(context=cntxt, request=request))


def pages_in_work(request, work_id):
    pages = Page.objects.filter(parent_work=work_id)
    tmplt = loader.get_template('calligraphy/pages.html')
    cntxt = {'pages': pages}
    return HttpResponse(tmplt.render(context=cntxt, request=request))


def individual_page(request, page_id):
    page = Page.objects.get(id=page_id)
    chars = Character.objects.filter(parent_page=page_id)
    tmplt = loader.get_template('calligraphy/page.html')
    cntxt = {'chars': chars}
    return HttpResponse(tmplt.render(context=cntxt, request=request))


def individual_char(request, char_id):
    char = Character.objects.get(id=char_id)
    tmplt = loader.get_template('calligraphy/char.html')
    cntxt = {'char': char}
    return HttpResponse(tmplt.render(context=cntxt, request=request))


def page_i(request):
    return HttpResponse("Image Request")


def char_i(request):
    return HttpResponse("Character Request")

