# Generated by Django 4.2.3 on 2023-07-21 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Event_Management_App', '0005_alter_perdoruesjoinsevent_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perdoruesjoinsevent',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Event_Management_App.event'),
        ),
        migrations.AlterField(
            model_name='perdoruesjoinsevent',
            name='perdorues',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Event_Management_App.perdorues'),
        ),
    ]