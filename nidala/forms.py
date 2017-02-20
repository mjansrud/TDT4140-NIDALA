from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        error_msg = "Email or password is wrong"
        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    self.add_error('email',
                                   'The account is not confirmed. Click forgot password to receive a new confirmation email')
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
            print("Could not login user with email: {}".format(email))
