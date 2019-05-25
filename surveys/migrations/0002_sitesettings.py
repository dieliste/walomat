# Generated by Django 2.2 on 2019-05-25 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('welcome_text', models.TextField(default='Hello!', verbose_name='welcome text')),
                ('welcome_text_de', models.TextField(default='Hello!', null=True, verbose_name='welcome text')),
                ('welcome_text_en', models.TextField(default='Hello!', null=True, verbose_name='welcome text')),
            ],
            options={
                'verbose_name': 'site settings',
                'verbose_name_plural': 'site settings',
            },
        ),
    ]
