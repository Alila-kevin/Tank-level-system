# Generated by Django 5.1.2 on 2024-11-02 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TankLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tank', models.CharField(max_length=100)),
                ('level', models.FloatField()),
                ('time', models.DateTimeField()),
            ],
        ),
    ]
