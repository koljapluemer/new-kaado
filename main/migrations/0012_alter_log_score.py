# Generated by Django 4.2 on 2023-04-11 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_card_child_cards_alter_card_connected_cards_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
