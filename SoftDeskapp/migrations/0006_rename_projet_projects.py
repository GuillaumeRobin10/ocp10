# Generated by Django 3.2.5 on 2021-07-23 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SoftDeskapp', '0005_remove_projet_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Projet',
            new_name='Projects',
        ),
    ]
