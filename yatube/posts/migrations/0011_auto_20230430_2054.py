# Generated by Django 2.2.16 on 2023-04-30 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_preferences'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='preferences',
            options={'default_related_name': 'preferences'},
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='group',
        ),
        migrations.AddField(
            model_name='preferences',
            name='group',
            field=models.ManyToManyField(related_name='preferences', to='posts.Group'),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to=settings.AUTH_USER_MODEL),
        ),
    ]
