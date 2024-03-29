# Generated by Django 3.2.14 on 2023-08-08 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nasheeds', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedNasheed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('nasheed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nasheeds.nasheed', verbose_name='Nasheed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'saved nasheed',
                'verbose_name_plural': 'saved nasheeds',
            },
        ),
        migrations.AddConstraint(
            model_name='savednasheed',
            constraint=models.UniqueConstraint(fields=('user', 'nasheed'), name='unique user and nasheed relation'),
        ),
    ]
