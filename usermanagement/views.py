from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, render, Http404
from post_office import mail

from usermanagement.forms import *
from usermanagement.models import *


def login_view(request):

    """
    View for logging the user in.
    If the login form is valid, log the user in and redirect to the requested page
    """

    if request.user.is_authenticated:
        raise Http404

    if request.method == 'POST':
        next = request.POST.get('next')
        form = LoginForm(request.POST)
        if form.is_valid():
            form.authenticate_user(request)
            if request.POST.get('next') == None or request.POST.get('next') == 'None':
                return HttpResponseRedirect(reverse('subjects'))
            else:
                return HttpResponseRedirect(request.POST.get('next'))
    else:
        form = LoginForm()
        next = request.GET.get('next')

    context = {
        'form': form,
        'next': next
    }

    return render(request, 'usermanagement/login.html', context)


def logout_view(request):

    """
    View for logging the user out
    """

    logout(request)
    return HttpResponseRedirect(reverse('index'))


def signup_view(request):

    """
    View for signing up new users. If the signup form is valid,
    create a new unactivated user and send them an email for activation.
    """

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.create_user()
            user = User.objects.get(email=form.cleaned_data.get('email'))
            token = UserToken.objects.create(user=user)
            mail.send(recipients=[user.email],
                      sender=settings.DEFAULT_FROM_MAIL,
                      template='activation_email',
                      context={'request': request, 'user': user, 'token': token})
            messages.add_message(request, messages.INFO,
                                 'You will receive a confirmation email to verify your email address')
            return HttpResponseRedirect(reverse('index'))

    else:
        form = SignUpForm()

    context = {
        'form': form
    }

    return render(request, 'usermanagement/signup.html', context)


def forgot_password_view(request):

    """
    View where users can get a new password.
    Sends a unique temporary link to the user where they can reset their password.
    """

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data.get('email'))
            token = UserToken.objects.create(user=user)
            if not user.is_active:
                mail.send(recipients=[user.email],
                          sender=settings.DEFAULT_FROM_MAIL,
                          template='activation_email',
                          context={'request': request, 'user': user, 'token': token})
                messages.add_message(request, messages.INFO,
                                     'You will receive a confirmation email to verify you email address')
            else:
                mail.send(recipients=[user.email],
                          sender=settings.DEFAULT_FROM_MAIL,
                          template='set_password_email',
                          context={'request': request, 'user': user, 'token': token})
                messages.add_message(request, messages.INFO,
                                     'You will receive an email with further instruction to reset your password')

            return HttpResponseRedirect(reverse('index'))
    else:
        form = ForgotPasswordForm()

    context = {
        'form': form
    }

    return render(request, 'usermanagement/forgot_password.html', context)


def change_password_view(request):
    if not request.user.is_authenticated:
        raise Http404

    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, email=request.user.email)
        if form.is_valid():
            form.change_password(request)
            messages.add_message(request, messages.INFO, 'The password is now changed')
            return HttpResponseRedirect(reverse('index'))

    else:
        form = ChangePasswordForm(email=request.user.email)

    context = {
        'form': form
    }

    return render(request, 'usermanagement/change_password.html', context)


def activate(request, key):

    """
    View for activating new users. After signup the users receive an email with a link to this view.
    """

    try:
        token = UserToken.objects.get(key=key)
        token.activate()
        messages.add_message(request, messages.INFO, 'Your account is now activated')
        return HttpResponseRedirect(reverse('index'))
    except UserToken.DoesNotExist:
        raise Http404


def set_password_view(request, key):

    """
    View where users can set a new password. When a user uses the forgot password view,
    it will receive an email with a unique temporary link to this view.
    """

    try:
        token = UserToken.objects.get(key=key)
    except UserToken.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            token.set_password(form.cleaned_data.get('new_password'))
            messages.add_message(request, messages.INFO, 'The new password is now set')
            return HttpResponseRedirect(reverse('index'))

    else:
        form = SetPasswordForm()

    context = {
        'form': form,
        'key': key,
    }

    return render(request, 'usermanagement/set_password.html', context)
