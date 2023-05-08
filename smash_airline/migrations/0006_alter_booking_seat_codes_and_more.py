# Generated by Django 4.1.6 on 2023-05-02 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smash_airline', '0005_alter_booking_seat_codes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='seat_codes',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='passengerseatinfo',
            name='booking_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smash_airline.booking'),
        ),
    ]