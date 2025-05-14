from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from main.models import Car, Sale


def cars_list_view(request):
    # список авто
    template_name = 'main/list.html'
    # поисковый запрос из GET-параметра 'q' указан в html шаблоне
    search_query = request.GET.get('q', '')

    if search_query:
        # поиск (без учета регистра)
        cars = Car.objects.filter(
            Q(model__icontains=search_query) |
            Q(color__icontains=search_query) |
            Q(year__icontains=search_query)
        ).order_by('-year', 'model')
    else:
        cars = Car.objects.all().order_by('-year', 'model')

    # Пагинация - 3 объекта на страницу
    page_number = request.GET.get('page', 1)
    paginator = Paginator(cars, 3)
    try:
        current_page = paginator.page(page_number)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    # page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': current_page,
        'search_query': search_query
    }
    # без пагинации
    # context = {
    #     'cars': cars,
    #     'search_query': search_query  # Передаем запрос для отображения в форме
    # }

    return render(request, template_name, context)


def car_details_view(request, car_id):
    # получить объект, если его нет, ошибка 404
    template_name = 'main/details.html'
    car = get_object_or_404(Car, id=car_id)
    context = {
        'car': car,
    }
    return render(request, template_name, context)


def sales_by_car(request, car_id):
    try:
        # получение объекта авто и его продаж или 404
        template_name = 'main/sales.html'
        car = get_object_or_404(Car, id=car_id)
        sales = Sale.objects.filter(car=car).select_related('client').order_by('-created_at')

        paginator = Paginator(sales, 5)  # 5 на страницу
        page_number = request.GET.get('page')
        sales_page = paginator.get_page(page_number)

        context = {
            'car': car,
            'sales': sales_page
        }
        return render(request, template_name, context)

    except Car.DoesNotExist:
        raise Http404('Car not found')


def home_view(request):
    return render(request, 'main/home.html')

def about_view(request):
    return render(request, 'main/about.html')

def contacts_view(request):
    return render(request, 'main/contacts.html')
