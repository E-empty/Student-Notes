# Generated by Django 4.1.7 on 2023-03-27 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_note_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]