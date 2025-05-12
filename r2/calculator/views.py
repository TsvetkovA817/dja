from datetime import datetime
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}

DATA2 = {
    'omlet': {
        'name': 'Омлет',
        'desc': 'Классический пышный омлет',
    },
    'pasta': {
        'name': 'Паста',
        'desc': 'Паста с сыром',
    },
    'buter': {
        'name': 'Бутерброд',
        'desc': 'Вкусный бутерброд с колбасой и сыром',
    },
}

def home_view(request):

    pages = {'Главная страница': reverse('home'),
             'О нас': reverse('about'),
             'Контакты': reverse('contacts'),
             }
    template_name = 'calculator/index.html'

    # Добавляем блюда из DATA (DATA2 для названия)
    # for dish_key in DATA.keys():
    #     dish_name = DATA2.get(dish_key, {}).get('name', dish_key.capitalize())
    #     pages[dish_name] = reverse('recipe', kwargs={'dish': dish_key})

    # Получаем номер страницы из GET-параметра
    page_number = request.GET.get('page', 1)

    # Создаем список блюд для пагинации
    dishes_list = list(DATA2.items())

    # Создаем пагинатор (3 блюда на страницу)
    paginator = Paginator(dishes_list, 3)

    try:
        current_page = paginator.page(page_number)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {
        'pages': pages,
        'dishes_page': current_page,
    }
    # context = {
    #     'pages': pages,
    #     'dishes_info': DATA2   # блюда для списка на главной без пагинации
    # }
    return render(request, template_name, context)


def recipe_view(request, dish):

    pages = {
        'Главная страница': reverse('home'),
        'О нас': reverse('about'),
        'Контакты': reverse('contacts'),
    }

    servings = int(request.GET.get('servings', 1))
    recipe = DATA.get(dish, {})

    # Умножаем количество ингредиентов на число порций
    adjusted_recipe = {}
    for ingredient, amount in recipe.items():
        adjusted_recipe[ingredient] = round(amount * servings, 2)

    context = {
        'recipe': adjusted_recipe,
        'dish_name': DATA2.get(dish, {}).get('name', dish.capitalize()),
        'dish_desc': DATA2.get(dish, {}).get('desc', ''),
        'servings': servings,
        'home_url': reverse('home'),
        'pages': pages,
    }
    return render(request, 'calculator/index.html', context)


def about_view(request):
    pages = {
        'Главная страница': reverse('home'),
        'О нас': reverse('about'),
        'Контакты': reverse('contacts'),
    }
    template_name = 'calculator/about.html'

    context = {
        'pages': pages,
        'current_page': 'about'
    }
    return render(request, template_name, context)


def contacts_view(request):
    pages = {
        'Главная страница': reverse('home'),
        'О нас': reverse('about'),
        'Контакты': reverse('contacts'),
    }
    template_name = 'calculator/contacts.html'

    context = {
        'pages': pages,
        'current_page': 'contacts'
    }
    return render(request, template_name, context)
