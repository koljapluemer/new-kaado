# Generated by Django 4.2 on 2023-04-06 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_log_input_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='input_type',
            field=models.IntegerField(blank=True, default=99, null=True),
        ),
    ]
