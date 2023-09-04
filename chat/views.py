from django.shortcuts import render


def lobby(request, room):
    return render(request, "chat/public.html", {"room_name": ""})