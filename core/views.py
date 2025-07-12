from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as app_login, logout as app_logout
from django.contrib import messages

# Login view
def login(request):
    return render(request, "login.html")

# Submit login view
def submit_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            app_login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Usuário/Senha inválidos.")
    return redirect("login")

# Logout view
def logout(request):
    app_logout(request)
    return redirect("login")
