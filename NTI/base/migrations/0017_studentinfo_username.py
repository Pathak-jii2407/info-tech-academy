# Generated by Django 5.0.2 on 2024-05-31 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_studentinfo_subject_teacheraccount_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinfo',
            name='username',
            field=models.CharField(default=datetime.datetime(2024, 5, 31, 15, 59, 58, 474197, tzinfo=datetime.timezone.utc), max_length=40),
            preserve_default=False,
        ),
    ]
