from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import UserRegisterForm

def index(request):
    return render(request, 'quiz/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Після успішної реєстрації перенаправляємо на вхід
    else:
        form = UserRegisterForm()
    return render(request, 'quiz/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('index')