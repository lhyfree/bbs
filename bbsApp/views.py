# Create your views here.
import time,os,sys,string,urllib
from models import Comment,Post
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from mongoengine.django.auth import User
from django.contrib import auth
from django.core.mail import send_mail

def test(request):
    return HttpResponse("3")

def index(request):
    posts = Post.objects()
    return render_to_response("index.html",{'posts':posts},context_instance=RequestContext(request))

@login_required
def edit(request):
    error = False
    if request.method == 'POST':
        spub_date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        stitle = request.POST.get('title')
        if not stitle :
            error = True
            return render_to_response("edit.html",{'error':error},context_instance=RequestContext(request))
        else:
            scontent = request.POST.get('content')
            sauthor = request.user.username
            post = Post(title = stitle,content = scontent,author = sauthor,date = spub_date)
            post.save()
            return HttpResponseRedirect("/")
    else:
        return render_to_response("edit.html",{'error':error},context_instance=RequestContext(request))

def post_id(request,offset):
    try:
        post = Post.objects(id=offset).first()
    except Exception,e:
        print e
        raise Http404()
    return render_to_response("post_id.html",{'post':post},context_instance=RequestContext(request))

def comment(request):
    if request.method == 'POST':
        scontent = request.POST.get('content')
        spost_id = request.POST.get('post_id')
        if not scontent:
            return HttpResponseRedirect("/")
        comment_date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        sauthor = request.POST.get('author')
        c = Post.objects.get(id = spost_id)
        scomment = Comment(author = sauthor,content = scontent,date = comment_date)
        c.comment.append(scomment)
        c.save()
        return HttpResponseRedirect("/"+spost_id+"/")

@login_required
def post_id_edit(request,offset1,offset2):
    try:
        post = Post.objects(id=offset1).first()
    except Exception,e:
        print e
        raise Http404()
    error = False
    print '------'
    if post.author == offset2:
        if request.method == 'POST':
            spub_date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
            stitle = request.POST.get('title')
            print '------',stitle
            if not stitle :
                error = True
                return render_to_response("post_id_edit.html",{'post':post,'error':error},context_instance=RequestContext(request))
            else:
                scontent = request.POST.get('content')
                post.update(set__title = stitle,set__content = scontent,set__date = spub_date)
                post.save()
                return HttpResponseRedirect("/"+offset1+"/")
        else:
            return render_to_response("post_id_edit.html",{'post':post,'error':error},context_instance=RequestContext(request))
    else:
        raise Http404()


@login_required
def post_id_delete(request,offset1,offset2):
    try:
        post = Post.objects(id=offset1).first()
    except Exception,e:
        print e
        raise Http404()
    if post.author == offset2:
        post.delete()
        return HttpResponseRedirect("/")
    else:
        raise Http404()

@login_required
def modify(request):
    flag = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print username,password
        try:
            user =  User.objects.get(username=username)
        except Exception,e:
            print e
            raise Http404()
        user.set_password(password)
        flag = True
        return render_to_response("modify.html",{'flag':flag},context_instance=RequestContext(request))
    else:
        return render_to_response("modify.html",{'flag':flag},context_instance=RequestContext(request))

def findpassword(request):
    flag = 0
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user =  User.objects.get(username=username,email=email)
            print user.password
            send_mail('Your password',user.password,'focuslhy@gmail.com',[user.email], fail_silently=False)
        except Exception,e:
            flag = 1
            return render_to_response("findpassword.html",{'flag':flag},context_instance=RequestContext(request))
        flag = 2
    return render_to_response("findpassword.html",{'flag':flag},context_instance=RequestContext(request))

def login(request):
    error = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            error = True
            return render_to_response("registration/login.html",{'error':error},context_instance=RequestContext(request))
    else:
        return render_to_response("registration/login.html",{'error':error},context_instance=RequestContext(request))

def register(request):
    error = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects(username=username)
        if not username or not password or not email or not len(user)==0 :
            error = True
            return render_to_response("registration/register.html",{'error':error},context_instance=RequestContext(request))
        else:
            User.create_user(username=username, password=password,email=email)
            newuser = auth.authenticate(username=username, password=password)
            auth.login(request, newuser)
            return HttpResponseRedirect("/")
    else:
        return render_to_response("registration/register.html",{'error':error},context_instance=RequestContext(request))

def about(request):
    return render_to_response("about.html",context_instance=RequestContext(request))