#
# Logic of application goes here:  Receive Request -> Process -> Serve Response
#
###################################################

from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from .models import Author, Work, Page, Character, RelatedChars, UserSuppliedPageMultiplier, CharSet, FlagForReview
from .models import ToDrawBoxesWBoxes
import json
import subprocess as sub
import random

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail

def draw_chars(request):
    tmplt = loader.get_template('calligraphy/draw_chars.html')
    return HttpResponse(tmplt.render(request=request))

def webroot(request):
    tmplt = loader.get_template('calligraphy/view_root.html')
    cntxt = {'user': request.user}
    return HttpResponse(tmplt.render(context=cntxt, request=request))

def validate_root(request):
    tmplt = loader.get_template('calligraphy/validate_root.html')
    return HttpResponse(tmplt.render(request=request))
    
def validate_find_offsets(request):
    tmplt = loader.get_template('calligraphy/validate_find_offsets.html')
    return HttpResponse(tmplt.render(request=request))

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
        charList.append({'charId' : char.id,
                         'pageId' : char.parent_page.id,
                         'authorId' : char.parent_author.id,
                         'authorName': char.author_name,
                         'workId' : char.parent_work.id,
                         'URL' : Character.get_image(char),
                         'mark' : char.mark,
                         'x1' : char.x1,
                         'y1' : char.y1,
                         'x2' : char.x2,
                         'y2' : char.y2})

    data = { 'pageId' : page_id,
              'URL' : Page.get_image(page),
              'height' : page.image_length,
              'width' : page.image_width,
              'chars' : charList}
    return JsonResponse(data, safe=False)
    
    
def get_to_verify_page(request):
    choice_from_list = random.choice(ToDrawBoxesWBoxes.objects.all())
    page = Page.objects.get(id=choice_from_list.toCheck.id)
    chars = Character.objects.filter(parent_page=page)
    charList = []
    for char in chars:
        charList.append({'charId' : char.id,
                         'URL' : Character.get_image(char),
                         'mark' : char.mark,
                         'x1' : char.x1,
                         'y1' : char.y1,
                         'x2' : char.x2,
                         'y2' : char.y2,
                         'x_thumb': char.image_width,
                         'y_thumb': char.image_height,
                         'area': (char.x2 - char.x1) * (char.y2 - char.y1)})
    charList.sort(key=lambda k: k['area'], reverse=True)

    data = {  'toDoId' : choice_from_list.id,
              'pageId' : page.id,
              'URL' : Page.get_image(page),
              'height' : page.image_length,
              'width' : page.image_width,
              'chars' : charList}
    return JsonResponse(data, safe=False)

@csrf_exempt
def get_char_relatives(request):
    char_id = request.GET.get('charId', None)
    curChar = Character.objects.get(id=char_id)
    chars_rel = Character.get_rel_chars(curChar)
    charList = []
    for char in chars_rel:
        charList.append({
            'URL': str(Character.get_image(char)),
            'uWidth': char.x2 - char.x1,
            'uHeight': char.y2 - char.y1,
            'id': char.id,
        })
    return JsonResponse(charList, safe=False)

@csrf_exempt
def get_root_tree(request):
    author = request.POST.get('id', None)
    response = []
    if author is None:     #Root request
        authors = Author.objects.all()
        for author in authors:
            response.append({
                'id':       str(author.id).zfill(4),
                'name':     author.name,
                'isParent': 'true'
        })
    else:
        if len(author) == 4:
            works = Work.objects.filter(author=int(author))
            for work in works:
                if work.title != "?":                               #TODO: enable this but include a filter option for clarity
                    response.append({
                        'id':          author + str(work.id).zfill(4),
                        'name':        work.title,
                        'isParent':    'true'
            })
        else:
            wrkid = int(author[4:])
            pages = Page.objects.filter(parent_work=wrkid)
            for page in pages:
                response.append({
                    'id':       author + str(page.id).zfill(5),
                    'name':     str(page.id),
                    'isParent': 'false'
                    })
    return JsonResponse(response, safe=False)

@csrf_exempt
def validate_ajax(request):
    author = request.POST.get('id', None)
    response = []
    pages = Page.objects.filter(parent_work=wrkid)
    for page in pages:
        response.append({
            'id':       str(page.id).zfill(5),
            'name':     str(page.id),
            'isParent': 'false'
        })
    return JsonResponse(response, safe=False)
    
@csrf_exempt
def get_toshi(request):
    pageId = int(request.GET.get('id', None))
    cutNum = request.GET.get('num', None)
    page = Page.objects.get(id=pageId)
    ret = sub.run(['toshi-segment', str(page.image), cutNum], stdout=sub.PIPE, universal_newlines=True)
    chars = ret.stdout.split('\n')
    charlist = []
    if ret.returncode == 0:
        for char in chars:
            if len(char) > 10:
                data = char.split('@ ')[1].split(' ** ')
                xy = data[0].split(' ')
                x_mid = int(xy[0].strip('x:'))
                y_mid = int(xy[1].strip('y:'))
                ofs = data[1].split(' | ')
                of_top = int(ofs[0].strip('to_top:'))
                of_bottom = int(ofs[1].strip('to_bottom:'))
                of_left = int(ofs[2].strip('to_left:'))
                of_right = int(ofs[3].strip('to_right:'))
                charlist.append({'charId' : 0,
                    'pageId' : 0,
                    'authorId' : 0,
                    'authorName': '#',
                    'workId' : 0,
                    'URL' : '#',
                    'mark' : '#',
                    'x1' : x_mid - of_left,
                    'y1' : y_mid - of_top,
                    'x2' : x_mid + of_right,
                    'y2' : y_mid + of_bottom})
    return JsonResponse(charlist, safe=False)


@require_http_methods(['POST'])
def post_offsets(request):
    pst = json.loads(request.body)
    if pst['modified'] is True:
        user_mult = UserSuppliedPageMultiplier.objects.get(id=pst['mult_id'])
        user_mult.rotation = pst['rotation']
        user_mult.save()
        CharSet.objects.filter(userSupplied=user_mult).delete()
        for chars in pst['Char_sets']:
            charray = []
            for char in chars['Chars']:
                charray.append(Character.objects.get(id=char['id']))
            myset = CharSet(userSupplied=user_mult,
                set_offset_x = chars['xmult'],
                set_offset_y = chars['ymult'],
                set_valid    = bool(chars['Chars_valid']),
                )
            myset.save()
            for char in charray:
                myset.set_chars.add(char)
            myset.save()
    else:
        ToValidateOffsets.objects.get(id=pst['choice_id']).delete()
    

    return JsonResponse({"status" : "Done"})
    
@require_http_methods(['POST'])
def post_characters(request):
    pst = json.loads(request.body)
    page_id = int(pst['page_id'])
    mypage = Page.objects.get(id=page_id)
    parent_work = Work.objects.get(id=mypage.parent_work.id)
    parent_author = Author.objects.get(id=parent_work.author.id)
    updated = False

    if pst['flagged_for_review']:
        newFlag = FlagForReview(flagged_by = request.user,
                      parent_page = mypage)
        newFlag.save()
    else:
        if pst['modified']:
            updated = True
            for modChar in pst['modified_boxes']:
                tChar = Character.objects.get(id=modChar['charId'])
                tChar.x1 = int(modChar['x_top'])
                tChar.y1 = int(modChar['y_top'])
                tChar.x2 = int(modChar['x_len']) + int(modChar['y_top'])
                tChar.y2 = int(modChar['y_len']) + int(modChar['y_top'])
                tChar.save()
        if pst['deleted']:
            updated = True
            for delchar in pst['deleted_boxes']:
                Character.objects.get(id=delchar['charId']).delete()

        if pst['added']:
            updated = True
            for newChar in pst['new_boxes']:
                x_1 = int(newChar['x_top'])
                y_1 = int(newChar['y_top'])
                x_2 = int(newChar['x_len']) + int(newChar['x_top'])
                y_2 = int(newChar['y_len']) + int(newChar['y_top'])
                new_char = Character(supplied_by = request.user,
                                    parent_page = mypage,
                                    x1 = x_1,
                                    y1 = y_1,
                                    x2 = x_2,
                                    y2 = y_2,
                                    parent_author = parent_author,
                                    parent_work = parent_work)
                new_char.save()
    if not updated:
        ToDrawBoxesWBoxes.objects.get(id=pst['to_do_id']).delete()
    return JsonResponse({"status" : "Done"})
