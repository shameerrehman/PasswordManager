from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(req):
    if req.method  == "POST":
        if "signup-form" in req.POST:
            username = req.POST.get("username")
            email = req.POST.get("email")
            password = req.POST.get("password")
            password2 = req.POST.get("password2")
            #if passwords dont match
            if password != password2:
                notif = "Passwords did not match, please try again."
                messages.error(req, notif)
                return HttpResponseRedirect(req.path)
            #if username isn't unique
            elif User.objects.filter(username=username).exists():
                notif = f"Account with username {username} exists, please pick a unique username."
                messages.error(req, notif)
                return HttpResponseRedirect(req.path)
            #if email isn't unique
            elif User.objects.filter(email=email).exists():
                notif = f"Account with email {email} exists, please pick a unique email."
                messages.error(req, notif)
                return HttpResponseRedirect(req.path)
            #validations pass
            else:
                User.objects.create_user(username, email, password)
                new_user = authenticate(req, username=username, password=password2)
                if new_user is not None:
                    login(req, new_user)
                    notif = f"Welcome {username}! Glad you're here."
                    messages.success(req, notif)
                    return HttpResponseRedirect(req.path)

        if "logout" in req.POST:
            logout(req)
            notif = f"Logout successful, see you next time!"
            messages.success(req, notif)
            return HttpResponseRedirect(req.path)
        if "login" in req.POST:
            username = req.POST.get("username")
            password = req.POST.get("password")
            new_login = authenticate(req, username=username, password=password)
            if new_login is None:
                notif = f"Login unsuccessful, invalid credentials."
                messages.error(req, notif)
                return HttpResponseRedirect(req.path)

    return render(req, "index.html", {})