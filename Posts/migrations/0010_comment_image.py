# Generated by Django 3.0.8 on 2020-07-24 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0009_pictrue'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='files', verbose_name='Zdjęcie'),
        ),
    ]