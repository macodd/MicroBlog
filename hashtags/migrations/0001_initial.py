# Generated by Django 3.0.5 on 2020-04-24 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=120)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
