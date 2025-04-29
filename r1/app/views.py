from datetime import datetime
import os
from django.conf import settings

from django.http import HttpResponse
from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    current_time = datetime.now().strftime("%H:%M:%S")
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    workdir = settings.BASE_DIR
    print(workdir)
    # Получаем список файлов и папок
    items = os.listdir(workdir)
    print(items)
    # Формируем HTML-ответ
    content = f"<h1>Содержимое рабочей директории ({workdir}):</h1><ul>"
    for item in items:
        content += f"<li>{item}</li>"
    content += "</ul>"
    return HttpResponse(content)

