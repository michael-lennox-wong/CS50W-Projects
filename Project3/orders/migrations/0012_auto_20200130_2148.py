# Generated by Django 2.0.3 on 2020-01-30 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_orderitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='dinnerplatter',
            name='menu_item_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='pizza',
            name='menu_item_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sub1',
            name='menu_item_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sub2',
            name='menu_item_id',
            field=models.IntegerField(null=True),
        ),
    ]
