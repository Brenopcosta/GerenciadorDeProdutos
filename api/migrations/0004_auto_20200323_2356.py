# Generated by Django 3.0.4 on 2020-03-24 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200323_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='dataDeCriacao',
            field=models.DateField(auto_now_add=True),
        ),
    ]
