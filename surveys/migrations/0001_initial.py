# Generated by Django 2.2 on 2019-04-16 09:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('title_de', models.CharField(max_length=255, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='title')),
                ('accessible_from', models.DateTimeField(default=django.utils.timezone.now, verbose_name='accessible from')),
                ('accessible_to', models.DateTimeField(default=django.utils.timezone.now, verbose_name='accessible to')),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
            ],
            options={
                'verbose_name': 'election',
                'verbose_name_plural': 'elections',
            },
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=127, verbose_name='topic')),
                ('topic_de', models.CharField(max_length=127, null=True, verbose_name='topic')),
                ('topic_en', models.CharField(max_length=127, null=True, verbose_name='topic')),
                ('thesis', models.TextField(verbose_name='text')),
                ('thesis_de', models.TextField(null=True, verbose_name='text')),
                ('thesis_en', models.TextField(null=True, verbose_name='text')),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Election', verbose_name='election')),
            ],
            options={
                'verbose_name': 'thesis',
                'verbose_name_plural': 'theses',
            },
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=127, unique=True, verbose_name='short name')),
                ('full_name', models.CharField(max_length=255, verbose_name='full name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='parties/', verbose_name='image')),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Election', verbose_name='election')),
            ],
            options={
                'verbose_name': 'party',
                'verbose_name_plural': 'parties',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stance', models.IntegerField(choices=[(1, 'agree'), (2, 'neutral'), (3, 'disagree')], verbose_name='stance')),
                ('reasoning', models.TextField(verbose_name='reasoning')),
                ('reasoning_de', models.TextField(null=True, verbose_name='reasoning')),
                ('reasoning_en', models.TextField(null=True, verbose_name='reasoning')),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Party', verbose_name='party')),
                ('thesis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Thesis', verbose_name='thesis')),
            ],
            options={
                'verbose_name': 'answer',
                'verbose_name_plural': 'answers',
                'unique_together': {('party', 'thesis', 'stance')},
            },
        ),
    ]
