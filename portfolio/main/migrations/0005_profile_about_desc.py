# Generated by Django 5.2.1 on 2025-06-27 09:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_blogcategory_contactmessage_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about_desc',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
