# -*- coding:UTF-8 -*-
import time,os,sys,string,urllib
import random
import hashlib
from django.http import HttpResponse,Http404
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import Log,Comment,Category,Tag
from django.views.decorators.csrf import csrf_exempt

def test(request,offset):
    offset = urllib.unquote(offset)
    s = sys.getdefaultencoding()
    #offset = urllib.unquote(offset).encode('ascii')
    return HttpResponse(offset+s)

def index(request):
    return render_to_response("index.html",context_instance=RequestContext(request))

def blog(request):
    return HttpResponseRedirect("/blog/")

def blog_list(request):
    log_list = Log.objects.all()
    tag_list = Tag.objects.all()
    return render_to_response("list.html",{'log_list':log_list,'tag_list':tag_list},context_instance=RequestContext(request))

def blog_category(request,offset):
    try:
        c = Category.objects.get(id = int(offset))
    except Category.DoesNotExist:
        print offset," Category isn't in the database yet."
        raise Http404()
    log_list = Log.objects.filter(category_id=c.id)
    tag_list = Tag.objects.all()
    return render_to_response("list.html",{'log_list':log_list,'tag_list':tag_list},context_instance=RequestContext(request))

def blog_category_num(request):
    c3 =len( Log.objects.filter(category_id=3))
    c4 =len( Log.objects.filter(category_id=4))
    c5 =len( Log.objects.filter(category_id=5))
    c6 =len( Log.objects.filter(category_id=6))
    c7 =len( Log.objects.filter(category_id=7))
    c8 =len( Log.objects.filter(category_id=8))
    c9 =len( Log.objects.filter(category_id=9))
    c10 =len( Log.objects.filter(category_id=10))
    res = [c3,c4,c5,c6,c7,c8,c9,c10]
    print res
    return HttpResponse(res)

def blog_tag(request,offset):
    try:
        t = Tag.objects.get(id = int(offset))
    except Tag.DoesNotExist:
        print offset," Tag isn't in the database yet."
        raise Http404()
    log_list = Log.objects.filter(taglist__contains = t.id)
    tag_list = Tag.objects.all()
    return render_to_response("list.html",{'log_list':log_list,'tag_list':tag_list},context_instance=RequestContext(request))

def blog_id(request,offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    try:
        log = Log.objects.get(id=offset)
    except Log.DoesNotExist:
        print offset," Log isn't in the database yet."
        raise Http404()
    category = Category.objects.get(id=log.category_id).category
    tags = ''
    if  log.taglist:
        taglist = log.taglist.split(',')
        for i in taglist:
            t = Tag.objects.get(id=i)
            tags = tags + t.tag + ' '
        tags = tags[:-1]
    try:
        comments = Comment.objects.filter(log_id=str(offset))
    except Comment.DoesNotExist:
        comments = ''
        print offset," comment isn't in the database yet."
    return render_to_response("blog_id.html",{'log':log ,'category':category,'tags':tags,'comments':comments},
                              context_instance=RequestContext(request))

@login_required
def blog_id_edit(request,offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    try:
        log = Log.objects.get(id=offset)
    except Log.DoesNotExist:
        print offset," Log isn't in the database yet."
        raise Http404()
    error = False
    tags = ''
    category = Category.objects.get(id=int(log.category_id))
    categorylist1 = Category.objects.filter(parent_id='1')
    categorylist2 = Category.objects.filter(parent_id='2')
    if  log.taglist:
        taglist = log.taglist.split(',')
        for i in taglist:
            t = Tag.objects.get(id=i)
            tags = tags + t.tag + ' '
        tags = tags[:-1]
    if request.method == 'POST':
        spub_date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        stitle = request.POST.get('title')
        if not stitle :
            error = True
            return render_to_response("blog_id_edit.html",{'error':error,'category':category,'tags':tags,
                                                           'categorylist1':categorylist1,'categorylist2':categorylist2,'log':log},
                                      context_instance=RequestContext(request))
        else:
            _tags = request.POST.get('tags')
            _stags = ''
            if _tags:
                _taglist = _tags.split()
                for _tag in _taglist:
                    try:
                        _t=Tag.objects.get(tag=_tag)
                        _stags = _stags + str(_t.id) + ','
                    except Tag.DoesNotExist:
                        _tt = Tag(tag = _tag)
                        _tt.save()
                        _stags = _stags + str(_tt.id) + ','
                _stags = _stags[:-1]
            scontent = request.POST.get('content')
            scategoryid = request.POST.get('categoryid')
            sreporter = request.user.username
            log.title = stitle
            log.content = scontent
            log.reporter = sreporter
            log.pub_date = spub_date
            log.category_id = scategoryid
            log.taglist = _stags
            log.save()
            return HttpResponseRedirect("/blog/"+str(offset)+"/")
    else:
        return render_to_response("blog_id_edit.html",{'error':error,'category':category,'tags':tags,
                                                       'categorylist1':categorylist1,'categorylist2':categorylist2,'log':log},
                                  context_instance=RequestContext(request))

def blog_comment(request):
    if request.method == 'POST':
        comment_date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        susername = request.POST.get('username')
        semail = request.POST.get('email')
        scontent = request.POST.get('content')
        slog_id = request.POST.get('log_id')
        scomment = Comment(username = susername,email = semail,content = scontent,date = comment_date,log_id = slog_id)
        scomment.save()
        return HttpResponseRedirect("/blog/"+slog_id+"/")

@login_required
def blog_edit(request):
    error = False
    categorylist1 = Category.objects.filter(parent_id='1')
    categorylist2 = Category.objects.filter(parent_id='2')
    if request.method == 'POST':
        spub_date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        stitle = request.POST.get('title')
        if not stitle :
            error = True
            return render_to_response("edit.html",{'error':error,'categorylist1':categorylist1,'categorylist2':categorylist2},
                                      context_instance=RequestContext(request))
        else:
            scontent = request.POST.get('content')
            sreporter = request.user.username
            categoryid = request.POST.get('categoryid')
            tags = request.POST.get('tags')
            stags = ''
            if tags:
                taglist = tags.split()
                for tag in taglist:
                    try:
                        t=Tag.objects.get(tag=tag)
                        stags = stags + str(t.id) + ','
                    except Tag.DoesNotExist:
                        tt = Tag(tag = tag)
                        tt.save()
                        stags = stags + str(tt.id) + ','
                stags = stags[:-1]
            log = Log(title = stitle,content = scontent,reporter = sreporter,pub_date = spub_date,category_id = categoryid,taglist = stags)
            log.save()
            return HttpResponseRedirect("/blog/list/")
    else:
        return render_to_response("edit.html",{'error':error,'categorylist1':categorylist1,'categorylist2':categorylist2},
                                  context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/blog/")
    else:
        form = UserCreationForm()
        return render_to_response("registration/register.html", { 'form': form},
                              context_instance=RequestContext(request))
def photo(request):
    if sys.platform == 'win32':
        d = ''
    else:
        from bae.api import bcs
        HOST = 'http://bcs.duapp.com/'
        AK = '0Fee62285c9d0eb1460505d929aa73d3'
        SK = '56120a1ee1fc47755592b4d9b7b99952'
        bbcs = bcs.BaeBCS(HOST, AK, SK)
        bucketName = "focusfree"
        prefix = '/upload/images/'
        e,d = bbcs.list_objects(bucketName,prefix)
        if e == 0:
            pass
        else:
            print 'bcs error.'
    return render_to_response("photo.html",{'d':d},context_instance=RequestContext(request))

@csrf_exempt
def upload_photo(request):
    ret="0"
    new_name=''
    _file = request.FILES.get('Filedata', None)
    if _file:
        result,new_name=profile_upload(_file)
        if result:
            ret = 'Successful'
        else:
            ret = 'Failed'
    json={'ret':ret,'save_name':new_name}
    return HttpResponse(ret)

def profile_upload(_file):
    date = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    rand = str(random.randint(1, 10000)) + date + str(_file)
    hashlib.md5().update(rand)
    file_name = hashlib.md5(rand).hexdigest()
    file_ext='.jpg'
    if sys.platform == 'win32':
        if _file:
            path = os.path.join(os.path.dirname(__file__), '..').replace('\\','/') + '/static/upload/images/'
            file_ext=os.path.splitext(_file.name)[1].lower()
            if not os.path.exists(path):
                os.mkdir(path)
            path_file=os.path.join(path,file_name+file_ext)
            upload_files_ext = ['.gif','.jpg','.jpeg','.png','.bmp']
            if file_ext not in upload_files_ext:
                return (False,file_name+file_ext)
            fp = open(path_file, 'wb')
            for content in _file.chunks():
                fp.write(content)
            fp.close()
            return (True,file_name+file_ext) #change
        else:
            return (False,file_name+file_ext)   #change
    else:
        if _file:
            from bae.api import bcs
            try:
                HOST = 'http://bcs.duapp.com/'
                AK = '0Fee62285c9d0eb1460505d929aa73d3'
                SK = '56120a1ee1fc47755592b4d9b7b99952'
                bbcs = bcs.BaeBCS(HOST, AK, SK)
                bucketName = "focusfree"
                saveFileName = '/upload/images/' + file_name + file_ext
                saveFileData = _file
                e,d = bbcs.put_object(bucketName, saveFileName, saveFileData)
                if e == 0:
                    return (True,file_name+file_ext)
                else:
                    return (False,file_name+file_ext)
            except:
                return (False,file_name+file_ext)
        else:
            return (False,file_name+file_ext)


@csrf_exempt
def profile_delte(request):
    del_file=request.POST.get("delete_file",'')
    if del_file:
        path_file=os.path.join(settings.STATICFILES_DIRS,'upload','images',del_file)
        os.remove(path_file)

def music(request):
    return render_to_response("music.html",context_instance=RequestContext(request))

def video(request):
    return render_to_response("video.html",context_instance=RequestContext(request))

def about(request):
    return render_to_response("about.html",context_instance=RequestContext(request))

def about_me(request):
    return render_to_response("me.html",context_instance=RequestContext(request))