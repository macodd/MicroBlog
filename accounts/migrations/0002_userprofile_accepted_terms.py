# Generated by Django 3.0.5 on 2020-05-06 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='accepted_terms',
            field=models.BooleanField(default=False),
        ),
    ]
