# Generated by Django 5.0.6 on 2024-06-06 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Prediction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorData1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nutrient1', models.FloatField()),
                ('nutrient2', models.FloatField()),
                ('nutrient3', models.FloatField()),
                ('nutrient4', models.FloatField()),
                ('nutrient5', models.FloatField()),
                ('nutrient6', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
