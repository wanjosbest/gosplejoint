from django import forms
from django.contrib.auth.forms import SetPasswordForm

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email Address", max_length=254)
    
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label=("New Password"),
        help_text=("Your new password must contain at least 8 characters."),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label=("Confirm Password"),
        help_text=("Enter the same password as before, for verification."),
    )

# class UploadSongForm(forms.ModelForm)
#     class Meta:
#         model = Post
#         fields = ["title", "body","categories","image","slug","upload_song","meta_keywords","meta_descriptions","genres"]
#         widget = {
#             "title": forms.TextInput(atrrs ={"class":"form-control","placeholder":"Song Title"}),
#         }