from django.test import TestCase, Client
from django.urls import reverse
from .models import Recipe, Category


class MainViewTestCase(TestCase):
    """Тести для view main - 10 випадкових рецептів"""

    def setUp(self):
        """Підготовка тестових даних"""
        self.client = Client()
        self.category = Category.objects.create(name='Закуски')

        # Створюємо 15 рецептів
        for i in range(15):
            Recipe.objects.create(
                title=f'Рецепт {i + 1}',
                description=f'Опис рецепту {i + 1}',
                instructions=f'Інструкції {i + 1}',
                ingredients=f'Інгредієнти {i + 1}',
                category=self.category
            )

    def test_main_view_returns_200(self):
        """Тест: View повертає статус 200"""
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_main_view_uses_main_template(self):
        """Тест: View використовує шаблон main.html"""
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, 'main.html')

    def test_main_view_returns_10_recipes(self):
        """Тест: View повертає максимум 10 рецептів"""
        response = self.client.get(reverse('main'))
        recipes = response.context['recipes']
        self.assertLessEqual(len(recipes), 10)

    def test_main_view_recipes_not_empty(self):
        """Тест: Список рецептів не порожній"""
        response = self.client.get(reverse('main'))
        recipes = response.context['recipes']
        self.assertGreater(len(recipes), 0)


class CategoryDetailViewTestCase(TestCase):
    """Тести для view category_detail - рецепти категорії"""

    def setUp(self):
        """Підготовка тестових даних"""
        self.client = Client()
        self.category = Category.objects.create(name='Супи')
        self.another_category = Category.objects.create(name='Салати')

        # Рецепти першої категорії
        for i in range(5):
            Recipe.objects.create(
                title=f'Суп {i + 1}',
                description=f'Опис супу {i + 1}',
                instructions=f'Інструкції {i + 1}',
                ingredients=f'Інгредієнти {i + 1}',
                category=self.category
            )

        # Рецепти другої категорії
        for i in range(3):
            Recipe.objects.create(
                title=f'Салат {i + 1}',
                description=f'Опис салату {i + 1}',
                instructions=f'Інструкції {i + 1}',
                ingredients=f'Інгредієнти {i + 1}',
                category=self.another_category
            )

    def test_category_detail_view_returns_200(self):
        """Тест: View повертає статус 200"""
        response = self.client.get(
            reverse('category_detail', args=[self.category.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_category_detail_view_uses_template(self):
        """Тест: View використовує шаблон category_detail.html"""
        response = self.client.get(
            reverse('category_detail', args=[self.category.id])
        )
        self.assertTemplateUsed(response, 'category_detail.html')

    def test_category_detail_view_returns_correct_category(self):
        """Тест: View повертає правильну категорію"""
        response = self.client.get(
            reverse('category_detail', args=[self.category.id])
        )
        self.assertEqual(response.context['category'].id, self.category.id)

    def test_category_detail_view_returns_only_category_recipes(self):
        """Тест: View повертає тільки рецепти цієї категорії"""
        response = self.client.get(
            reverse('category_detail', args=[self.category.id])
        )
        recipes = response.context['recipes']

        # Перевіряємо що всі рецепти належать цій категорії
        for recipe in recipes:
            self.assertEqual(recipe.category.id, self.category.id)

        # Перевіряємо кількість
        self.assertEqual(len(recipes), 5)

    def test_category_detail_view_recipes_count(self):
        """Тест: Кількість рецептів першої категорії = 5"""
        response = self.client.get(
            reverse('category_detail', args=[self.category.id])
        )
        recipes = response.context['recipes']
        self.assertEqual(len(recipes), 5)

    def test_category_detail_view_different_categories(self):
        """Тест: Для різних категорій повертаються різні рецепти"""
        # Для першої категорії
        response1 = self.client.get(
            reverse('category_detail', args=[self.category.id])
        )
        recipes1 = response1.context['recipes']

        # Для другої категорії
        response2 = self.client.get(
            reverse('category_detail', args=[self.another_category.id])
        )
        recipes2 = response2.context['recipes']

        # Кількість різна
        self.assertNotEqual(len(recipes1), len(recipes2))
        self.assertEqual(len(recipes1), 5)
        self.assertEqual(len(recipes2), 3)