# Generated by Django 3.2.12 on 2022-04-16 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='mfr_part_num',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
