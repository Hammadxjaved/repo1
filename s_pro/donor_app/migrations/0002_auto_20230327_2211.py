# Generated by Django 3.0.5 on 2023-03-27 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor_health',
            name='hemoglobin_level',
            field=models.IntegerField(),
        ),
    ]
