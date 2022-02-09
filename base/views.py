from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import RoomForm, TopicForm


rooms = [
    {'id': 1, 'name': 'Learn Django'},
    {'id': 2, 'name': 'Learn Javascript'},
    {'id': 3, 'name': 'Learn css'},


]
'''
key = 'id'
key = [dict[key] for dict in rooms]
print('key ', key)
for k in key:
    print(k, end=' '),
'''

context = {
    'rooms': rooms
}

key = 'name'
key = [dict[key] for dict in rooms]
print('key ', key)
for k in key:
    print(k, end=' '),


def room(request):

    search = request.GET.get('search')
    if search == None:
        search = ''

    rooms = Room.objects.filter(topic__name__icontains=search)

    rooms_count = rooms.count()
    if not rooms:
        rooms = Room.objects.all()
        rooms_count = rooms.count()
    topics = Topic.objects.all()

    context = {
        'rooms': rooms,
        'topics': topics,
        'rooms_count': rooms_count,

    }

    return render(request, 'base/room.html', context)


def room_detail(request, pk):
    '''
    room = None
    for i in rooms:
        if i['id'] == pk:
            room = i
    context = {
        "room": room
    }
    return render(request, 'base/detail.html', context)
    Message model
    host = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    # topic =
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    # participants =
    update = models.DateTimeField(auto_now=datetime.now)
    created = models.DateTimeField(auto_now_add=True)

    '''

    #mess = Message.objects.get(host=request.user)
    room = Room.objects.get(id=pk)

    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == "POST":
        message1 = Message.objects.create(
            host=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)

        return redirect('detail', pk=room.id)

    for value in request.POST:
        print(value)
        print(request.user)
    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants


    }

    return render(request, 'base/detail.html', context)


@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        RoomForm()
        return redirect('room')

    return render(request, 'base/room_form.html', {'form': form})


@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)

    # So we can save the room instance that we are going to
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':   # update.
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()

            return redirect('room')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def deleteRoom(request, pk):

    room = Room.objects.get(id=pk)
    room.delete()
    return redirect('room')

    return render(request, 'base/room_form.html')


@login_required(login_url='/login')
def deleteConfirm(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    # return redirect('room')
    return render(request, 'base/delete_confirm.html', {'room': room})


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('room')

    first = "first"
    if request.method == "POST":

        username = request.POST["username"]

        print('username', username)
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('room')
        else:
            messages.error(request, 'User or Password is incorrect')

        context = {
            "username": username,
            "password": password,
            "page": page,
        }

    else:
        context = {
            "first": first,
            "page": page
        }
    print('page: ', page)
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('room')


def registerUser(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.username
        user.save()
        form.save()
        login(request, user)
        return redirect('room')
    else:
        messages.error(request, 'An error occurred during registration.')
    form = UserCreationForm()
    return render(request, 'base/login_register.html', {'form': form})


def createMessage(request, pk):
    pass
