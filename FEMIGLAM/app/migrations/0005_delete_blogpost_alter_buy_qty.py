# Generated by Django 5.1.4 on 2025-02-25 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_blogpost'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BlogPost',
        ),
        migrations.AlterField(
            model_name='buy',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]
