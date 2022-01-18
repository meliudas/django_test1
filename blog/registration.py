import json
import threading
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from validate_email import validate_email
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse

from blog.forms import LoginForm
from blog.models import Category, Author, Comment, CustomUser
from blog.parameters import SITE_PROTOCOL, SITE_URL

from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django__0003.utils import token_generator


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authentification/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    if not settings.TESTING:
        EmailThread(email).start()


def registration(request):
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'Password should be at least 6 characters')
            context['has_error'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'Password mismatch')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Enter a valid email address')
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True

        if CustomUser.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'Username is taken, choose another one')
            context['has_error'] = True

            return render(request, 'registration.html', context, status=409)

        if CustomUser.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Email is taken, choose another one')
            context['has_error'] = True

            return render(request, 'registration.html', context, status=409)

        if context['has_error']:
            return render(request, 'registration.html', context)

        user = CustomUser.objects.create_user(username=username, email=email, password=password2)
        user.set_password(password2)
        user.is_active = False
        user.save()

        if not context['has_error']:
            send_activation_email(user, request)

            messages.add_message(request, messages.SUCCESS,
                                 'We sent you an email to verify your account')
            return redirect('login')

    return render(request, 'registration.html')


def activate_user(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))

        user = CustomUser.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and token_generator.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))

    return render(request, 'authentification/activate-failed.html', {"user": user})


def sign_in(request):
    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and not user.is_email_verified:
                messages.add_message(request, messages.ERROR,
                                     'Email is not verified, please check your email inbox')
                return render(request, 'login.html', context, status=401)

            if not user:
                messages.add_message(request, messages.ERROR,
                                     'Invalid credentials, try again')
                return render(request, 'login.html', context, status=401)

            login(request, user)

            messages.add_message(request, messages.SUCCESS,
                                 f'Welcome {user.username}')

            return redirect(reverse('index'))
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)

    messages.add_message(request, messages.SUCCESS,
                         'Successfully logged out')
