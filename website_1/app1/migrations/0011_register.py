# Generated by Django 4.2.3 on 2023-08-06 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_alter_finepage_url_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('mail', models.CharField(max_length=100)),
                ('number', models.FloatField()),
                ('password', models.CharField(max_length=30)),
            ],
        ),
    ]
