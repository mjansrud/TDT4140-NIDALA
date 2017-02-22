from django.contrib.auth.models import User
from django.contrib.auth import login
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-post', max_length=100)
    password = forms.CharField(label='Passord', max_length=100, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        error_msg = "E-posten eller passordet er feil"
        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    self.add_error('email',
                                   'Brukeren er ikke aktivert. Trykk på glemt passord for å motta en ny e-post')
                    return
            except User.DoesNotExist:
                self.add_error('email', error_msg)
                self.add_error('password', error_msg)
                return

            if not user.check_password(password):
                self.add_error('email', error_msg)
                self.add_error('password', error_msg)

    def authenticate_user(self, request):
        email = self.cleaned_data.get("email")
        try:
            user = User.objects.get(email=email)
            login(request, user)
        except User.DoesNotExist:
            print("Kan ikke logge inn brukeren med e-post: {}".format(email))


class SignUpForm(forms.Form):
    first_name = forms.CharField(label='Fornavn', max_length=255)
    last_name = forms.CharField(label='Etternavn', max_length=255)
    email = forms.EmailField(label='E-post', max_length=255)
    password = forms.CharField(label='Passord', max_length=255, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Bekreft passord', max_length=255, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        try:
            User.objects.get(email=email)
            self.add_error('email', 'E-posten er allerede registrert')
        except User.DoesNotExist:
            pass

        if password != confirm_password:
            msg = 'Passordene er ikke like'
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)

        if not check_password(password):
            self.add_error('password',
                           'Passordet må være minst 8 tegn, inneholde minst et tall og en stor bokstav')

    def create_user(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = User.objects.create(username=email,
                                   email=email,
                                   first_name=first_name,
                                   last_name=last_name,
                                   is_active=False)
        user.set_password(password)
        user.save()


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(label='E-post', max_length=100)

    def clean(self):
        cleaned_data = super(ForgotPasswordForm, self).clean()
        email = cleaned_data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.add_error('email', 'E-posten er ikke registrert')


class SetPasswordForm(forms.Form):
    new_password = forms.CharField(label='Nytt passord', max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Bekreft passord', max_length=100, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(SetPasswordForm, self).clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            self.add_error('new_password', 'Passordene er ikke like')
            self.add_error('confirm_password', 'Passordene er ikke like')

        if not check_password(new_password):
            self.add_error('new_password',
                           'Passordet må være minst 8 tegn, inneholde minst et tall og en stor bokstav')


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label='Nåværende passord', max_length=100, widget=forms.PasswordInput)
    new_password = forms.CharField(label='Nytt passord', max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Bekreft passord', max_length=100, widget=forms.PasswordInput)

    def __init__(self, email, *args, **kwargs):
        self.email = email
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        email = self.email

        user = User.objects.get(email=email)

        if not user.check_password(current_password):
            self.add_error('current_password', 'Feil passord')

        if new_password != confirm_password:
            self.add_error('new_password', 'Passordene er ikke like')
            self.add_error('confirm_password', 'Passordene er ikke like')

        if not check_password(new_password):
            self.add_error('new_password',
                           'Passordet må være minst 8 tegn, inneholde minst et tall og en stor bokstav')

    def change_password(self, request):
        email = self.email
        new_password = self.cleaned_data.get('new_password')
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        login(request, user)


def check_password(password):
    # To short password
    if len(password) < 8:
        return False

    # No capital letter
    if password.lower() == password:
        return False

    # Check for at least a digit
    digit = False
    for ch in password:
        if ch.isdigit():
            digit = True

    if not digit:
        return False

    return True
