# Generated by Django 3.0.5 on 2020-05-16 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='images/default_avatar.jpg', null=True, upload_to='images/'),
        ),
    ]
