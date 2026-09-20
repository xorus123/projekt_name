from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Quiz, Question, QuizResult
from .forms import QuizForm, QuestionForm


# 1. ГОЛОВНА СТОРІНКА ТА ПОШУК
def index(request):
    query = request.GET.get('q', '')  # Отримуємо пошуковий запит
    if query:
        # Шукаємо за назвою або описом
        quizzes = Quiz.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        # Показуємо всі вікторини (нові спочатку)
        quizzes = Quiz.objects.all().order_by('-id')
        
    return render(request, 'quiz/index.html', {
        'quizzes': quizzes,
        'query': query
    })


# 2. РЕЄСТРАЦІЯ КОРИСТУВАЧА
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Одразу авторизуємо після реєстрації
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/register.html', {'form': form})


# 3. ВИХІД З АКАУНТУ
def custom_logout(request):
    logout(request)
    return redirect('index')


# 4. СТВОРЕННЯ ВІКТОРИНИ
@login_required(login_url='login')
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = request.user  # Прив'язуємо автора
            quiz.save()
            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'quiz/create_quiz.html', {'form': form})


# 5. ДОДАВАННЯ ПИТАНЬ ДО ВІКТОРИНИ
@login_required(login_url='login')
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            
            # Якщо натиснули "Додати ще питання"
            if 'add_another' in request.POST:
                return redirect('add_question', quiz_id=quiz.id)
            # Якщо натиснули "Завершити"
            return redirect('index')
    else:
        form = QuestionForm()
    return render(request, 'quiz/add_question.html', {'form': form, 'quiz': quiz})


# 6. ПРОХОДЖЕННЯ ВІКТОРИНИ
@login_required(login_url='login')
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    
    if request.method == 'POST':
        score = 0
        # Перевіряємо відповіді
        for q in questions:
            selected_option = request.POST.get(f'question_{q.id}')
            if selected_option and int(selected_option) == q.correct_option:
                score += 1
        
        # Зберігаємо результат у базу даних
        result = QuizResult.objects.create(
            quiz=quiz,
            user=request.user,
            score=score,
            total_questions=questions.count()
        )
        return redirect('quiz_result', result_id=result.id)
        
    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions': questions})


# 7. СТОРІНКА РЕЗУЛЬТАТУ
@login_required(login_url='login')
def quiz_result(request, result_id):
    result = get_object_or_404(QuizResult, id=result_id, user=request.user)
    return render(request, 'quiz/quiz_result.html', {'result': result})


# 8. ТАБЛИЦЯ ЛІДЕРІВ
def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # Беремо топ-10 кращих результатів
    results = QuizResult.objects.filter(quiz=quiz).order_by('-score', 'date_completed')[:10]
    return render(request, 'quiz/leaderboard.html', {'quiz': quiz, 'results': results})


# 9. РЕДАГУВАННЯ ВІКТОРИНИ (тільки для автора)
@login_required(login_url='login')
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quiz/create_quiz.html', {'form': form, 'edit_mode': True})


# 10. ВИДАЛЕННЯ ВІКТОРИНИ (тільки для автора)
@login_required(login_url='login')
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, author=request.user)
    quiz.delete()
    return redirect('index')