# Generated by Django 3.2 on 2023-08-03 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_alter_recipeingredient_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rname_recipe_ingredients', to='recipes.ingredient', verbose_name='Название ингредиента'),
        ),
    ]
