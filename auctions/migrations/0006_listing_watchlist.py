# Generated by Django 4.2.3 on 2023-08-28 08:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_category_listing_alter_listing_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='cart', to=settings.AUTH_USER_MODEL),
        ),
    ]
