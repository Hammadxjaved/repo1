# Generated by Django 3.0.5 on 2023-03-28 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0004_auto_20230328_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient_details',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
