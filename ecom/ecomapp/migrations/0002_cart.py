# Generated by Django 5.0.4 on 2024-04-19 05:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.product')),
            ],
        ),
    ]
