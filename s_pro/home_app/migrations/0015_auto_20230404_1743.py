# Generated by Django 3.0.5 on 2023-04-04 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donor_app', '0009_donor_details_health'),
        ('home_app', '0014_blood_request_response_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blood_request_response',
            name='appointment_id',
        ),
        migrations.RemoveField(
            model_name='blood_request_response',
            name='date_of_request',
        ),
        migrations.RemoveField(
            model_name='blood_request_response',
            name='date_of_response',
        ),
        migrations.RemoveField(
            model_name='blood_request_response',
            name='img',
        ),
        migrations.RemoveField(
            model_name='blood_request_response',
            name='quantity',
        ),
        migrations.AddField(
            model_name='blood_request_response',
            name='req_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home_app.blood_request'),
        ),
        migrations.AlterField(
            model_name='blood_request_response',
            name='donor_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='donor_app.donor_details'),
        ),
    ]
