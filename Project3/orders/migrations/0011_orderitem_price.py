# Generated by Django 2.0.3 on 2020-01-30 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20200130_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
