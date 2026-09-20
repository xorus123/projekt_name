from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Quiz, Question

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Електронна пошта")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise forms.ValidationError("Пароль має містити щонайменше 8 символів!")
        return password

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']
        labels = {
            'title': 'Назва вікторини',
            'description': 'Опис вікторини'
        }

# НОВА ФОРМА ДЛЯ ЗАПИТАНЬ
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option1', 'option2', 'option3', 'option4', 'correct_option']
        labels = {
            'text': 'Текст запитання',
            'option1': 'Варіант 1',
            'option2': 'Варіант 2',
            'option3': 'Варіант 3',
            'option4': 'Варіант 4',
            'correct_option': 'Номер правильного варіанту'
        }