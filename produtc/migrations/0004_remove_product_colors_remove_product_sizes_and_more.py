# Generated by Django 5.0.6 on 2024-07-12 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produtc', '0003_color_size_product_colors_product_sizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='colors',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sizes',
        ),
        migrations.DeleteModel(
            name='Color',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
