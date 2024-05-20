# Generated by Django 5.0.4 on 2024-04-29 04:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0003_cart_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.product')),
                ('user', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
