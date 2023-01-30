from django import forms
from users.models import CustomUser

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
    # /// For forms.form
    # username = forms.CharField(max_length=200)
    # first_name = forms.CharField(max_length=200)
    # last_name = forms.CharField(max_length=200)
    # password = forms.CharField(max_length=128)
    # email = forms.EmailField()

    # def __init__(self, *args, **kwargs):
    #        super().__init__(*args, **kwargs)
    #        self.fields['username'].widget.attrs.update({'class': 'form-control'})
    #        self.fields['password'].widget.attrs.update({'class':'form-control'})

    def save(self, commit = False):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
        

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'image')
