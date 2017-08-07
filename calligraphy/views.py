#
# Logic of application goes here:  Receive Request -> Process -> Serve Response
#
###################################################

from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from django.core import serializers
from .models import Author, Work, Page, Character, RelatedChars, UserSuppliedPageMultiplier, CharSet, FlagForReview
from .models import ToDrawBoxesWBoxes, ToDrawBoxesWoBoxes, UserDid
from django.db.models import Count
import json
import subprocess as sub
import random

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail

from skimage import io, morphology, util, color, measure, filters, segmentation
from operator import attrgetter
import numpy as np

def view_progress(request):
    tmplt = loader.get_template('calligraphy/view_progress.html')
    return HttpResponse(tmplt.render(request=request))

def draw_chars(request, old_or_new):
    tmplt = loader.get_template('calligraphy/draw_chars.html')
    cntxt = {'old_or_new': old_or_new}
    return HttpResponse(tmplt.render(context=cntxt, request=request))
    
def eval_bad_pages(request):
    tmplt = loader.get_template('calligraphy/eval_bad_pages.html')
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
    parent_work = 0
    parent_author = 0
    charList = []
    for char in chars:
        if char.parent_author is None or char.parent_work is None:
            parent_work = 0
            parent_author = 0
        else:
            parent_work = char.parent_work.id
            parent_author = char.parent_author.id
        charList.append({'charId' : char.id,
                         'pageId' : char.parent_page.id,
                         'authorId' : parent_author,
                         'authorName': char.author_name,
                         'workId' : parent_work,
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
    pageNum = None
    choice = None
    choiceNumber = 0
    request_num = int(request.GET.get('old_or_new', None))
    if request_num == 1:     # WARNING:  MAGIC NUMBERS
        choice = random.choice(ToDrawBoxesWBoxes.objects.all())
        choiceNumber = choice.id
        pageNum = choice.toCheck.id
    else:
        if request_num == 0:
            choice = random.choice(ToDrawBoxesWoBoxes.objects.all())
            choiceNumber = choice.id
            pageNum = choice.toCheck.id
        else:
            pageNum = request_num
    page = Page.objects.get(id=pageNum)
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

    data = {  'toDoId' : choiceNumber,
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
def get_progress(request):
    pg_users = []
    pages = []
    ch_users = []
    chars = []
    remain_box = ToDrawBoxesWBoxes.objects.all().count()
    remain_no_box = ToDrawBoxesWoBoxes.objects.all().count()
    
    remaining = [ remain_box, remain_no_box ]
    remain_name = [ "remain_box", "remain_no_box" ]
    userds = UserDid.objects.annotate(Count('pages_changed'))
    for userd in userds:
        pg_users.append(userd.user_supplied.username)
        pages.append(userd.pages_changed__count)
    userds = UserDid.objects.annotate(Count('chars_changed'))
    for userd in userds:
        ch_users.append(userd.user_supplied.username)
        chars.append(userd.chars_changed__count)
    response = {"pg_names":             pg_users,
                "pages":                pages,
                "ch_names":             ch_users,
                "chars":                chars,
                "remain_name":          remain_name,
                "remaining":            remaining}
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

def get_me_some_boxes(img, white_chars):
    threshold = filters.threshold_li(img)
    if white_chars:
        bw =  img > threshold
    else:
        bw = img < threshold

       
    labels = measure.label(bw, connectivity=2)
    lbl_props = measure.regionprops(labels)
    sorted(lbl_props, key=lambda k: k['area'], reverse=True)
    charlist = []
    for prop in lbl_props:
        bbox = prop.bbox
        area = (bbox[3] - bbox[1]) * (bbox[2] - bbox[0])
        charlist.append({'charId' : 0,
                        'pageId' : 0,
                        'authorId' : 0,
                        'authorName': '#',
                        'workId' : 0,
                        'URL' : '#',
                        'mark' : '#',
                        'x1' : bbox[1],
                        'y1' : bbox[0],
                        'x2' : bbox[3],
                        'y2' : bbox[2],
                        'area': area,
                        'bbox': bbox})
    return charlist
    
def get_me_some_fast_boxes(img, iteration, white_chars):
    threshold = filters.threshold_li(img)
    if white_chars:
        bw =  img > threshold
    else:
        bw = img < threshold
    labels = measure.label(bw, connectivity=2)
    lbl_props = measure.regionprops(labels)
    sprops = sorted(lbl_props, key=attrgetter('area'))
    area_cutoff = int(sprops[len(sprops) - 1].area / 100)
    for prop in sprops:
        if prop.area < area_cutoff:
            np.putmask(bw, labels == prop.label, False)
        else:
            break
    for num in range(iteration):
        bw = morphology.dilation(bw)
    labels = measure.label(bw, connectivity=2)
    lbl_props = measure.regionprops(labels)
    charlist = []
    for prop in lbl_props:
        bbox = prop.bbox
        charlist.append({'charId' : 0,
                        'pageId' : 0,
                        'authorId' : 0,
                        'authorName': '#',
                        'workId' : 0,
                        'URL' : '#',
                        'mark' : '#',
                        'x1' : bbox[1],
                        'y1' : bbox[0],
                        'x2' : bbox[3],
                        'y2' : bbox[2],
                        'bbox': bbox})
    return charlist

def find_boxes(request):
    getdict = request.GET.dict()
    page_id = int(getdict['page_id'])
    white_chars = getdict['white_chars'] == 'true'
    iteration = int(getdict['iteration'])
    page = Page.objects.get(id=page_id)
    img = util.img_as_ubyte(color.rgb2grey(io.imread(page.get_image())))
    boxes = get_me_some_fast_boxes(img, iteration, white_chars)
        
    
    return JsonResponse({'chars': boxes}, safe=False)


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
    user_supss = UserDid.objects.filter(user_supplied=request.user)
    user_sups = None
    if len(user_supss) == 0:
        user_sups = UserDid(user_supplied=request.user)
        user_sups.save()
    else:
        user_sups = user_supss[0]
    pst = json.loads(request.body)
    page_id = int(pst['page_id'])
    updated = False
    mypage = Page.objects.get(id=page_id)
    to_draw_box_from_list = None
    if int(pst['old_or_new']) == 0:
        ToDrawBoxesWoBoxes.objects.get(id=pst['to_do_id']).delete()
        to_draw_box_from_list = ToDrawBoxesWBoxes(toCheck=mypage)
        to_draw_box_from_list.save()
        updated = True
    else:
        if int(pst['old_or_new']) == 1:
            to_draw_box_from_list = ToDrawBoxesWBoxes.objects.get(id=pst['to_do_id'])
    user_sups.pages_changed.add(mypage)
    parent_work = None
    parent_author = None
    if mypage.parent_work is not None:
        parent_work = Work.objects.get(id=mypage.parent_work.id)
        parent_author = Author.objects.get(id=parent_work.author.id)
    if pst['flagged_for_review']:
        newFlag = FlagForReview(flagged_by = request.user,
                      parent_page = mypage)
        newFlag.save()
    else:
        if pst['modified']:
            updated = True
            for modChar in pst['modified_boxes']:
                tChar = Character.objects.get(id=modChar['charId'])
                tChar.x1 = int(modChar['x_1'])
                tChar.y1 = int(modChar['y_1'])
                tChar.x2 = int(modChar['x_2'])
                tChar.y2 = int(modChar['y_2'])
                tChar.save()
                user_sups.chars_changed.add(tChar)
        if pst['deleted']:
            updated = True
            for delchar in pst['deleted_boxes']:
                Character.objects.get(id=delchar['charId']).delete()

        if pst['added']:
            updated = True
            if parent_work is None:
                for newChar in pst['new_boxes']:
                    new_char = Character(supplied_by = request.user,
                                         parent_page = mypage,
                                         x1 = int(newChar['x_1']),
                                         y1 = int(newChar['y_1']),
                                         x2 = int(newChar['x_2']),
                                         y2 = int(newChar['y_2']))
                    new_char.save()
                    user_sups.chars_changed.add(new_char)
            else:
                for newChar in pst['new_boxes']:
                    new_char = Character(supplied_by = request.user,
                                         parent_page = mypage,
                                         x1 = int(newChar['x_1']),
                                         y1 = int(newChar['y_1']),
                                         x2 = int(newChar['x_2']),
                                         y2 = int(newChar['y_2']),
                                         parent_author = parent_author,
                                         parent_work = parent_work)
                    new_char.save()
                    user_sups.chars_changed.add(new_char)
    if not updated:
        to_draw_box_from_list.delete()
    return JsonResponse({"status" : "Done"})


@csrf_exempt
def get_bad_pages(request):
    choice = random.choice(FlagForReview.objects.all())
    choiceNumber = choice.id
    pageNum = choice.parent_page.id
    page = Page.objects.get(id=pageNum)
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

    data = {  'toDoId' : choiceNumber,
              'pageId' : page.id,
              'URL' : Page.get_image(page),
              'height' : page.image_length,
              'width' : page.image_width,
              'chars' : charList}
    return JsonResponse(data, safe=False)
