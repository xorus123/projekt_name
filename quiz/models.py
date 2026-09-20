from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва вікторини")
    description = models.TextField(blank=True, verbose_name="Опис")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# НОВА МОДЕЛЬ ЗАПИТАННЯ
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', verbose_name="Вікторина")
    text = models.CharField(max_length=500, verbose_name="Текст запитання")
    option1 = models.CharField(max_length=200, verbose_name="Варіант 1")
    option2 = models.CharField(max_length=200, verbose_name="Варіант 2")
    option3 = models.CharField(max_length=200, verbose_name="Варіант 3")
    option4 = models.CharField(max_length=200, verbose_name="Варіант 4")
    correct_option = models.IntegerField(
        choices=[(1, 'Варіант 1'), (2, 'Варіант 2'), (3, 'Варіант 3'), (4, 'Варіант 4')],
        verbose_name="Правильна відповідь"
    )

    def __str__(self):
        return self.text
# Додай цю модель у самий кінець quiz/models.py
class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results', verbose_name="Вікторина")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    score = models.IntegerField(verbose_name="Набрані бали")
    total_questions = models.IntegerField(verbose_name="Всього запитань")
    date_completed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}/{self.total_questions}"