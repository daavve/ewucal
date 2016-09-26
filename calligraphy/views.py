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
# TODO:  Probably implement logging on so we can get rid of this

# TODO: Author list temporarily modified to only display authors that
#  Have works with annotated charactars

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

@csrf_exempt
def individual_page(request, page_id):
    if request.method == 'GET':
        page = Page.objects.get(id=page_id)
        tmplt = loader.get_template('calligraphy/page_new.html')
        cntxt = {'page': page}
        return HttpResponse(tmplt.render(context=cntxt, request=request))
    else:
        if request.method == 'POST':
            page_id = request.GET.get('docId', None)
            chars = Character.objects.filter(parent_page=8930)
            data = serializers.serialize("json", chars, safe=False)
            return HttpResponse(json.dump({"hi": "there"}, skipkeys=True), content_type='application/json'))
         
         
         
            
#          chars = Character.objects.filter(parent_page=page_id)
#         a_chars = []
#         for char in chars:
#           a_chars.append(RelatedChars(char))


