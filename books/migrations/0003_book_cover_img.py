# Generated by Django 4.1.5 on 2023-01-30 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_img',
            field=models.ImageField(default='cover.png', upload_to=''),
        ),
    ]