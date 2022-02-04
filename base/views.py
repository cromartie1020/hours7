from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        'rooms_count': rooms_count
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

    '''
    room = Room.objects.get(id=pk)
    context = {
        'room': room

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
    if request.user.is_authenticated:
        return redirect('room')

    first = "first"
    if request.method == "POST":

        username = request.POST["username"]
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
            "password": password
        }

    else:
        context = {
            "first": first
        }

    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('room')
