#Login through email

# from django import forms
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import get_user_model, authenticate

# User = get_user_model()

# class EmailAuthenticationForm(AuthenticationForm):
#     username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))

#     def clean(self):
#         email = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')

#         if email and password:
#             self.user_cache = authenticate(self.request, email=email, password=password)
#             if self.user_cache is None:
#                 raise forms.ValidationError(
#                     "Invalid email or password.",
#                     code='invalid_login',
#                 )
#             else:
#                 self.confirm_login_allowed(self.user_cache)

#         return self.cleaned_data
