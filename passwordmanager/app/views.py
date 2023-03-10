from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import random
from django.core.mail import send_mail
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
from .models import Password

import logging.config
logger = logging.getLogger(__name__)

browser = Browser()
browser.set_handle_robots(False)
fernet = Fernet(settings.KEY)

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

        elif "logout" in req.POST:
            notif = f"Logout successful, see you next time!"
            logout(req)
            messages.success(req, notif)
            return HttpResponseRedirect(req.path)
        elif "login" in req.POST:
            username = req.POST.get("username")
            password = req.POST.get("password")
            new_login = authenticate(req, username=username, password=password)
            if new_login is None:
                notif = f"Login unsuccessful, invalid credentials."
                messages.error(req, notif)
                return HttpResponseRedirect(req.path)
            else:
                code = str(random.randint(100000, 999999))
                global global_code
                global_code = code
                send_mail(
                    "SafePass Manager: Confirm Your Email",
                    f"Your verification code is: {code}. Dont share this code with others.",
                    settings.EMAIL_HOST_USER,
                    [new_login.email],
                    fail_silently=False,
                )
                return render(req, "index.html", 
                {
                    'code':code,
                    'user':new_login
                })
        elif "confirm" in req.POST:
            code_input = req.POST.get('code')
            user = req.POST.get('user')
            if code_input != global_code:
                notif = "Wrong code, please try logging in again."
                messages.error(req, notif)
                return HttpResponseRedirect(req.path)
            else:
                login(req, User.objects.get(username=user))
                notif = f"{req.user} welcome back!"
                messages.success(req, notif)
                return HttpResponseRedirect(req.path)

        elif "add-new-pass" in req.POST:
            url = req.POST.get('url')
            email = req.POST.get('email')
            password = req.POST.get('password')
            try:
                #encrypt user secrets
                encrypted_email = fernet.encrypt(email.encode())
                encrypted_password = fernet.encrypt(password.encode())
                #get url details
                browser.open(url)
                site_title = browser.title()
                #get favicon
                try:
                    site_favicon = favicon.get(url)[0].url
                except:
                    site_favicon = "https://cdn2.iconfinder.com/data/icons/pittogrammi/142/95-512.png"
                #save to DB
                new_password_entry = Password.objects.create(
                    user = req.user,
                    email = encrypted_email.decode(),
                    password = encrypted_password.decode(),
                    url = url,
                    title = site_title,
                    favicon = site_favicon
                )
                notif = f"{site_title} successfully added!"
                messages.success(req, notif)
            except:
                notif = f"Sorry, {url} is not compatible"
                messages.error(req, notif)
            return HttpResponseRedirect(req.path)
        elif "delete-pressed" in req.POST:
            delete_card = req.POST.get("password-id")
            notif = f"{Password.objects.get(id=delete_card).title} successfully deleted!"
            Password.objects.get(id=delete_card).delete()
            messages.success(req, notif)
            return HttpResponseRedirect(req.path)
        elif "update-pressed" in req.POST:
            update_card = req.POST.get("password-id")
            newUsername = req.POST.get("new-username")
            newPass = req.POST.get("new-password")
            encrypted_new_email = fernet.encrypt(newUsername.encode())
            encrypted_new_password = fernet.encrypt(newPass.encode())
            obj = Password.objects.get(id=update_card)
            obj.email = encrypted_new_email.decode()
            obj.password = encrypted_new_password.decode()
            obj.save()
            notif = f"{obj.title} successfully updated!"
            messages.success(req, notif)
            return HttpResponseRedirect(req.path)
    context={}
    if req.user.is_authenticated:
        all_passwords = Password.objects.all().filter(user = req.user)
        for password in all_passwords:
            password.email = fernet.decrypt(password.email.encode()).decode()
            password.password = fernet.decrypt(password.password.encode()).decode()
            
            context = {
                "all_passwords": all_passwords

            }
    return render(req, "index.html", context)