# Generated by Django 3.0.5 on 2023-03-28 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0002_auto_20230328_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='blood_request',
            name='bg_req',
            field=models.CharField(default='Z', max_length=3),
        ),
        migrations.AddField(
            model_name='blood_request_response',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
