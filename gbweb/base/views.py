from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import CodeRoom, Topic, Message
from .forms import CodeRoomForm

# Create your views here.

# coderooms = [
#     {'id' : 1, 'name': 'Gameboy code'},
#     {'id' : 2, 'name': 'Gameboy code2'},
#     {'id' : 3, 'name': 'Gameboy code3'},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User or Password does not exist')

    context = {'page': page}
    return render(request, 'base/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # commit False is to access the info and not auto commit
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'An error occured during registration')
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'base/login.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    coderooms = CodeRoom.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
    )  # give all rooms

    topics = Topic.objects.all()
    coderoom_count = coderooms.count()

    context = {'coderooms': coderooms, 'topics': topics,
               'coderoom_count': coderoom_count}
    return render(request, 'base/home.html', context)


def coderoom(request, pk):
    coderoom = CodeRoom.objects.get(id=pk)
    comments = coderoom.message_set.all().order_by('-created')

    if request.method == "POST":
        comments  = Message.objects.create(
            user =  request.user,
            coderoom = coderoom, 
            body = request.POST.get('body') # get from html
        )
        return redirect ('coderoom' , pk=coderoom.id)
        
    context = {'coderoom': coderoom, 'comments' : comments}
    return render(request, 'base/coderoom.html', context)


@login_required(login_url='login')
def createCodeRoom(request):
    if request.method == 'POST':
        form = CodeRoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = CodeRoomForm()
    context = {'form': form}
    return render(request, 'base/coderoom_form.html', context)


@login_required(login_url='login')
def updateCodeRoom(request, pk):
    coderoom = CodeRoom.objects.get(id=pk)
    form = CodeRoomForm(instance=coderoom)

    # not the room host
    if request.user != coderoom.host:
        return HttpResponse('You are not the room host')

    if request.method == 'POST':
        # instance is for what room to update
        form = CodeRoomForm(request.POST, instance=coderoom)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/coderoom_form.html', context)


def deleteCodeRoom(request, pk):
    coderoom = CodeRoom.objects.get(id=pk)

    if request.method == 'POST':
        coderoom.delete()
        return redirect('home')

    context = {'obj': coderoom}
    return render(request, 'base/delete.html', context)


def upload(request):
    if request.method == 'POST':
        form = CodeRoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    forms = CodeRoomForm()
    context = {'forms': forms}
    return render(request, 'base/coderoom_form.html', context)
