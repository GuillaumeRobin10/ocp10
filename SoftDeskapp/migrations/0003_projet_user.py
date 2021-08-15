# Generated by Django 3.2.5 on 2021-07-19 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SoftDeskapp', '0002_remove_projet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='projet',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
