# Generated by Django 5.0.6 on 2024-06-06 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Prediction', '0003_rename_sensordata1_sensordataa'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SensorDataa',
        ),
    ]