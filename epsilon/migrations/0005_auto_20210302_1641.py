# Generated by Django 3.1.7 on 2021-03-02 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epsilon', '0004_auto_20210302_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(default='', upload_to='question_pics'),
        ),
    ]
