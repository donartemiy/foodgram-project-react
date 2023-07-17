# from django.shortcuts import render
from django.http import HttpResponse


def index(request):    
    return HttpResponse('<h1>Главная страница</h1>')


def recipe_list(request):
    return HttpResponse('<h1>Список рецептов</h1>')


def recipe_detail(request, pk):
    return HttpResponse(f'<h1>Рецепт номер {pk}</h1>')
