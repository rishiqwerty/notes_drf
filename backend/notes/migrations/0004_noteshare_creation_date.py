# Generated by Django 5.0.1 on 2024-01-05 06:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_noteshare'),
    ]

    operations = [
        migrations.AddField(
            model_name='noteshare',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
