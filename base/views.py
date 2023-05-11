from ast import Or
from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import context
from .models import Room, Topic, Message, User
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, MyUserCreationForm

from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import MyUserCreationForm
from django.contrib import messages
from django.db.models import Q
# rooms = [
#     {'id': 1, "name": "Let's learn python"},
#     {'id': 2, "name": "Design with me"},
#     {'id': 3, "name": "Frontend devs"}
# ]


def loginPage(request):
    # if user is login but still want to do http://127.0.0.1:8000/login/, redirect user
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')
    # get the user and password
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST. get('password')
        # check if user and pw exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        # if the user exists, we check the credential
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # log user in and redirect user to home page
            # vvv login() create a session in database
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {"page": page}
    return render(request, 'login_register.html', context)


def logOut(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = "register"
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred while registration")
    context = {'page': page, "form": form}
    return render(request, "login_register.html", context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    rooms = Room.objects.filter(
        # Q allows us to add and or condition to the search
        # we are using or in this case
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]
    topics = Topic.objects.all()
    room_count = rooms.count()
    room
    context = {"rooms": rooms, "topics": topics,
               'room_count': room_count, "room_messages": room_messages}
    return render(request, 'home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('created')
    participants = room.participants.all()
    if request.method == "POST":
        room.participants.add(request.user)
        message = Message.objects.create(
            room=room,
            user=request.user,
            body=request.POST.get("body")
        )
        return redirect('room', pk=room.id)
    context = {"room": room, "room_messages": room_messages,
               "participants": participants}
    return render(request, 'room.html', context)


def userProfile(request, pk):
    # cái pk này là cái actual pk của user đó trong database
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    context = {"user": user, "rooms": rooms,
               "topics": topics, "room_messages": room_messages}
    return render(request, "profile.html", context)


# @login_required(login_url='login')
# def create_room(request):
#     form = RoomForm()
#     if request.method == "POST":
#         form = RoomForm(request.POST)
#         if form.is_valid:
#             room = form.save(commit=False)
#             # this make sure the room is created just based on the user who is logging in
#             # the form doesnot show available user and user can't pick who will log in
#             # it is automatically the person who is loggin in
#             room.host = request.user
#             room.save()
#             return redirect('home')

#     context = {"form": form}
#     return render(request, 'room_form.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("you are not allowed here !!!")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {"form": form}
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    # get the room
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("you are not allowed here !!!")
    if request.method == 'POST':
        # delete and then redirect back to home
        room.delete()
        return redirect('home')
    # render the html with the passed in room, notice room return str name room
    return render(request, "delete.html", {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("you are not allowed here !!!")
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, "delete.html", {'obj': message})
