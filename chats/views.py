from django.shortcuts import render

# Create your views here.

def index(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        username = request.POST.get('username')
        
        print(f"We received username {username} and  room name {room_name}")

    return render(request, 'chats/index.html' , { 'room_name': room_name, 'username': username })

def room(request, room_name, username):
    
    return render(request, 'chats/room.html', { 'room_name': room_name, 'username': username })