# Generated by Django 3.1.4 on 2021-07-22 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20210722_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='keywords',
            field=models.TextField(blank=True, null=True),
        ),
    ]
