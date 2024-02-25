# Generated by Django 4.2.4 on 2024-02-25 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0005_userprofile_location_userprofile_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='detail_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('main_image', models.ImageField(upload_to='main_images/')),
                ('detail_images', models.ManyToManyField(blank=True, to='authApp.detailimage')),
            ],
        ),
    ]
