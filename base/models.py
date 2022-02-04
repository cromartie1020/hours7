from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants=
    update = models.DateTimeField(auto_now=datetime.now)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    # topic =
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    # participants =
    update = models.DateTimeField(auto_now=datetime.now)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    return render(request, 'base/room_form.html', context)
