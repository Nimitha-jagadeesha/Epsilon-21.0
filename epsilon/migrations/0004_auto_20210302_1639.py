# Generated by Django 3.1.7 on 2021-03-02 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epsilon', '0003_auto_20210302_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(upload_to='question_pics'),
        ),
    ]
