from django import forms
from users.models import CustomUser

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
    # username = forms.CharField(max_length=200)
    # first_name = forms.CharField(max_length=200)
    # last_name = forms.CharField(max_length=200)
    # password = forms.CharField(max_length=128)
    # email = forms.EmailField()

    def save(self, commit = False):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
        

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'image')
