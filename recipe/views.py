from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Recipe, Category
import random


@require_http_methods(["GET"])
def main(request):
    """
    View для відображення 10 випадкових рецептів на головній сторінці
    """
    all_recipes = list(Recipe.objects.all())
    random_recipes = random.sample(all_recipes, min(10, len(all_recipes)))

    context = {
        'recipes': random_recipes
    }
    return render(request, 'main.html', context)


@require_http_methods(["GET"])
def category_detail(request, category_id):
    """
    View для відображення всіх рецептів певної категорії за її id
    """
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, '404.html', status=404)

    recipes = category.categories.all()

    context = {
        'category': category,
        'recipes': recipes
    }
    return render(request, 'category_detail.html', context)
