#
# Logic of application goes here:  Receive Request -> Process -> Serve Response
#
###################################################

from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from .models import Author, Work, Page, Character, RelatedChars, UserSuppliedPageMultiplier, CharSet, ToValidateOffsets, Char_location_update
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

# Here we give them everything at once.  We give them the page id, as well as all the data
def get_todo(request):
    choice_from_list = random.choice(ToValidateOffsets.objects.all())
    multiplier = UserSuppliedPageMultiplier.objects.get(id=choice_from_list.toCheck.id)
    page = Page.objects.get(id=multiplier.page_id.id)
    chars = Character.objects.filter(parent_page=page)
    charList = []
    for char in chars:
        coords = str(char.image).split('(')[1].split(')')[0].split(',')
        charList.append({'charId' : char.id,
                         'collection': 0,   # Placeholder
                         'mark': char.mark,
                         'URL' : Character.get_image(char),
                         'x1' : coords[0],
                         'y1' : coords[1],
                         'x2' : coords[2],
                         'y2' : coords[3],
                         'area': (int(coords[2]) - int(coords[0])) * (int(coords[3]) - int(coords[1]))})
                         
    charList.sort(key=lambda k: k['area'], reverse=True)
    setsData = []
    charsets = CharSet.objects.filter(userSupplied=multiplier)
    setNum = -1
    for charset in charsets:
        if charset.set_valid:
            setNum+=1
            curSet = setNum
        else:
            curSet = 3
        setsData.append({'set_multiplier': charset.set_offset_x,
                         'offset_x'  : 0,
                         'offset_y'  :  charset.set_offset_y - charset.set_offset_x,
                         'set_num'       : curSet})
        for char in charset.set_chars.all():
            for charL in charList:          # WARNING: O(i^j)
                if charL['charId'] == char.id:
                    charL['collection'] = setNum
        
    

    data = {  'pageId':   page.id,
              'URL' : Page.get_image(page),
              'height' : page.image_length,
              'width' : page.image_width,
              'chars' : charList,
              'mult_min': .3,
              'mult_max': 7,
              'rotation': multiplier.image_rotation,
              'mult_id': multiplier.id,
              'choice_id': choice_from_list.id,
              'set_data': setsData}
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


@require_http_methods(['POST']) # TODO:  some chars may still have bad offsets due to lack of ability to make new usermodified object for page that has not been modified previously.
# userId = request.user.id
 #c_page      = Page.objects.get(id=(pst['page_id'])) 
#    user_mult = UserSuppliedPageMultiplier( user_id=request.user, 
#                                            page_id=c_page, 
#                                            image_rotation=pst['rotation']) 
#    user_mult.save() 
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
    updated = False
    pst = json.loads(request.body)
    if pst['modified'] is True:
        updated = True
        for modChar in pst['modified_boxes']:
            tChar = Character.objects.get(id=modChar['charId'])
            x_1 = int(modChar['x_top'])
            y_1 = int(modChar['y_top'])
            x_2 = int(modChar['x_len']) + x_1
            y_2 = int(modChar['y_len']) + y_1
            mChar = Char_location_update(supplied_by = request.user,
                                         target_char = tChar,
                                         should_be_deleted = False,
                                         x1 = x_1,
                                         y1 = y_1,
                                         x2 = x_2,
                                         y2 = y_2)
            mChar.save()
                                         
    if pst['deleted'] is True:
        updated = True
        for delchar in pst['deleted_boxes']:
            tChar = Character.objects.get(id=delchar['charId'])
            dChar = Char_location_update(supplied_by = request.user,
                                         target_char = tChar,
                                         should_be_deleted = True,
                                         x1 = 0,
                                         x2 = 0,
                                         y1 = 0,
                                         y2 = 0)
            dChar.save()
            
    if pst['added'] is True:
        update = True
        page_id = int(pst['page_id'])
        mypage = Page.objects.get(id=page_id)
        for newChar in pst['new_boxes']:
            x_1 = int(newChar['x_top'])
            y_1 = int(newChar['y_top'])
            x_2 = int(newChar['x_len']) + x_1
            y_2 = int(newChar['y_len']) + y_1
            new_char = Character(supplied_by = request.user,
                                 parent_page = mypage,
                                 x1 = x_1,
                                 y1 = y_1,
                                 x2 = x_2,
                                 y2 = y_2)
            new_char.save()
    
    if update is False:
        ToDrawBoxesWBoxes.objects.get(id=pst['to_do_id']).delete()
    
    
    return JsonResponse({"status" : "Done"})
