# Generated by Django 2.2.12 on 2020-08-06 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='uname',
            field=models.CharField(default='anonymous', max_length=50),
            preserve_default=False,
        ),
    ]
