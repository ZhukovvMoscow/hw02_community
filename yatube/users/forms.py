from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Contact


User = get_user_model()


#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm
class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # укажем модель, с которой связана создаваемая форма
        model = User
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('first_name', 'last_name', 'username', 'email')


class PasswordChangingForm(PasswordChangeForm):
    fields = ('old_password', 'new_password1', 'new_password2')


class ContactForm(forms.ModelForm):
    class Meta:
        # На основе какой модели создаётся класс формы
        model = Contact
        # Укажем, какие поля будут в форме
        fields = ('name', 'email', 'subject', 'body')