# Generated by Django 4.2.3 on 2023-07-20 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Event_Management_App', '0002_alter_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to='pics'),
        ),
    ]
