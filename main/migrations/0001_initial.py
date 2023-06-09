# Generated by Django 2.2.7 on 2023-04-06 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('front', models.TextField()),
                ('back', models.TextField(null=True)),
                ('type', models.TextField(choices=[('Habit', 'habit'), ('Self Check-In', 'check'), ('Miscellaneous', 'misc'), ('Book', 'book'), ('Article', 'article'), ('Learning', 'learn'), ('Project', 'project')])),
                ('is_active', models.BooleanField(default=True)),
                ('is_priority', models.BooleanField(default=False)),
                ('is_started', models.BooleanField(default=False)),
                ('ease', models.FloatField(default=1)),
                ('repetitions', models.IntegerField(default=0)),
                ('occurrences', models.IntegerField(default=0)),
                ('interval', models.IntegerField(default=0)),
                ('interval_unit', models.CharField(default='d', max_length=1)),
                ('due_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Profile')),
                ('tags', models.ManyToManyField(to='main.Tag')),
            ],
        ),
    ]
