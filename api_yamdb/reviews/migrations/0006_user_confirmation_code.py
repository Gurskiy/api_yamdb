# Generated by Django 2.2.16 on 2022-04-27 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20220427_0559'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
    ]
