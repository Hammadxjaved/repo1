# Generated by Django 3.0.5 on 2023-03-31 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0007_remove_blood_request_response_appointment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blood_request',
            name='appointment_id',
        ),
        migrations.AddField(
            model_name='blood_request',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
