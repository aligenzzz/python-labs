# Generated by Django 4.2.1 on 2023-05-20 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_animal_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffer',
            name='username',
            field=models.CharField(default='', max_length=30),
        ),
    ]
