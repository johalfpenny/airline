# Generated by Django 4.1.6 on 2023-05-02 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smash_airline', '0004_alter_booking_email_alter_booking_number_tickets_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='seat_codes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='smash_airline.passengerseatinfo'),
        ),
    ]
