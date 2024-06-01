# Generated by Django 5.0.6 on 2024-05-26 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('name', models.CharField(max_length=100, verbose_name='従業員名')),
                ('department', models.CharField(max_length=100, verbose_name='部署')),
            ],
            options={
                'verbose_name_plural': '住所変更届',
            },
        ),
    ]