# Generated by Django 4.2 on 2023-04-12 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0012_alter_log_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='type',
            field=models.TextField(choices=[('habit', 'Habit'), ('check', 'Self Check-In'), ('todo', 'To-Do'), ('misc', 'Miscellaneous'), ('book', 'Book'), ('article', 'Article'), ('learn', 'Learn Card'), ('project', 'Project')]),
        ),
        migrations.AlterField(
            model_name='log',
            name='type',
            field=models.TextField(blank=True, choices=[('habit', 'Habit'), ('check', 'Self Check-In'), ('todo', 'To-Do'), ('misc', 'Miscellaneous'), ('book', 'Book'), ('article', 'Article'), ('learn', 'Learn Card'), ('project', 'Project')], null=True),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.card')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
