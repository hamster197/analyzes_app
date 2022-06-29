from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm
from django.core.exceptions import ValidationError

from analizes.models import *


class PathientRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser', 'is_active', 'is_staff', 'date_joined', 'groups',
                   'user_permissions', 'position', 'photo',]

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        exclude = []

class PathientEditForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser',  'is_staff', 'date_joined', 'groups',
                   'user_permissions', 'position', 'photo', ]

class DoctorNewForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser',  'is_staff', 'date_joined', 'groups',
                   'user_permissions', 'sport', 'age', 'height', 'weight', 'gender', 'phone',]

class DoctorEditForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        exclude = [ 'last_login', 'is_superuser',  'is_staff', 'date_joined', 'groups', 'password',
                   'user_permissions', 'sport',  'age', 'height', 'weight', 'gender', 'phone',]

class PswChangeForm(SetPasswordForm):
    class Meta:
        model = User
        exclude = []

class RecmendationEdit(forms.ModelForm):
    class Meta:
        model = RecomendationsQuide
        exclude =['type', 'patient', 'author',]

class RecomendationForm(forms.ModelForm):
    class Meta:
        model = RecomendationsQuide
        exclude = ['name', 'patient', 'author', 'attach', 'type' ]

class RecomendationFoodForm(forms.ModelForm):
    class Meta:
        model = RecomendationsQuide
        exclude = ['name', 'patient', 'author', 'type' ]

class RecomendationFoodQuideForm(forms.Form):
    name = forms.ModelChoiceField(queryset=RecomendationsQuide.objects.filter(author__groups__name='admins'),
                           label='Выберите рекомендацию:', required=True, )

class ChemicalElementsForm(forms.ModelForm):

    rezult = forms.FloatField(label='value', required=False)

    class Meta:
        model = ChemicalElementsMainQuide
        fields = ['name', 'required', 'size', ]

    def __init__(self, *args, **kwargs):
        super(ChemicalElementsForm, self).__init__(*args, **kwargs)
        if self['required'].value() == True:
            self.fields['rezult'].widget.attrs['required'] = True
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['required'].widget.attrs['onclick'] = 'return false;'
        self.fields['size'].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(ChemicalElementsForm, self).clean()
        if cleaned_data['required'] == True and cleaned_data['rezult'] == None:
                raise ValidationError('error!' , code='invalid')
        return

