# Generated by Django 3.2.25 on 2024-04-30 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20240430_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.CharField(choices=[('DR', 'Dress'), ('SH', 'Shirts'), ('ACC', 'Accessories')], max_length=3),
        ),
    ]