# Generated by Django 3.0.5 on 2023-03-28 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor_app', '0006_donor_details_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor_health',
            name='diabetic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='donor_health',
            name='disease',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='donor_health',
            name='preg',
            field=models.BooleanField(default=False),
        ),
    ]