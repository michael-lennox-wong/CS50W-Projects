# Generated by Django 2.0.3 on 2020-01-11 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_pasta'),
    ]

    operations = [
        migrations.CreateModel(
            name='DinnerPlatter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platter_type', models.CharField(choices=[('Ga', 'Garden Salad'), ('Gr', 'Greek Salad'), ('A', 'Antipasto'), ('BZ', 'Baked Ziti'), ('MP', 'Meatball Parm'), ('CP', 'Chicken Parm')], max_length=2)),
                ('size', models.CharField(max_length=1)),
            ],
        ),
    ]
