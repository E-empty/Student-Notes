# Generated by Django 4.1.7 on 2023-05-06 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_alter_note_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]