# Generated by Django 3.2.8 on 2021-11-13 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.CharField(choices=[('books', 'Books'), ('clothing', 'Clothing'), ('shoes', 'Shoes'), ('electronics', 'Electronics'), ('household products', 'Household products'), ('sports', 'Sports'), ('tourism', 'Tourism'), ('other', 'Other')], default=('other', 'Other'), max_length=64),
        ),
    ]
