# Generated by Django 4.1.7 on 2023-04-16 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='groups',
            field=models.ManyToManyField(to='authentication.mygroup'),
        ),
    ]