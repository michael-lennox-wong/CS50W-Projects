# Generated by Django 2.0.3 on 2020-01-29 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_menuitem_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='type',
            field=models.CharField(choices=[('Sa', 'Salad'), ('S1', 'Sub1'), ('S2', 'Sub2'), ('Pa', 'Pasta'), ('DP', 'DinnerPlatter'), ('Pi', 'Pizza')], default='Pi', max_length=2),
        ),
    ]
