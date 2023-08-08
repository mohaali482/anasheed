# Generated by Django 3.2.14 on 2023-08-08 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nasheeds', '0002_savednasheed'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='savednasheed',
            constraint=models.UniqueConstraint(fields=('user', 'nasheed'), name='unique user to nasheed relation'),
        ),
    ]
