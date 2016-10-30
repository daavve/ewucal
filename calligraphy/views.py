#
# Logic of application goes here:  Receive Request -> Process -> Serve Response
#
###################################################

from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from .models import Author, Work, Page, Character, RelatedChars
import json

from django.views.decorators.csrf import csrf_exempt

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


# NOTE: Not currently used
def individual_char(request, char_id):
    char = Character.objects.get(id=char_id)
    tmplt = loader.get_template('calligraphy/char.html')
    cntxt = {'char': char}
    return HttpResponse(tmplt.render(context=cntxt, request=request))

def individual_page(request, page_id):
    page = Page.objects.get(id=page_id)
    tmplt = loader.get_template('calligraphy/page.html')
    cntxt = {'page': page}
    return HttpResponse(tmplt.render(context=cntxt, request=request))

@csrf_exempt
def get_page(request):
    page_id = request.GET.get('pageId', None)
    page = Page.objects.get(id=page_id)
    chars = Character.objects.filter(parent_page=page_id)
    charList = []
    for char in chars:
        charList.append({"charId" : char.id,
                         "pageId" : char.parent_page.id,
                         "authorId" : char.parent_author.id,
                         "workId" : char.parent_work.id,
                         "URL" : Character.get_image(char),
                         "mark" : char.mark,
                         "x1" : char.x1,
                         "y1" : char.y1,
                         "x2" : char.x2,
                         "y2" : char.y2})

    data = { "pageId" : page_id,
              "URL" : Page.get_image(page),
              "height" : page.image_length,
              "width" : page.image_width,
              "chars" : charList}
    return JsonResponse(data, safe=False)
    
@csrf_exempt
def get_char_relatives(request):
    char_id = request.GET.get('charId', None)
    curChar = Character.objects.get(id=char_id)
    chars_rel = Character.get_rel_chars(curChar)
    charList = []
    for char in chars_rel:
        charList.append({
            'src': str(Character.get_image(char)),
            'id': char.id,
            'thumb': str(Character.get_thumb(char)),
        })
    return JsonResponse(charList, safe=False)


