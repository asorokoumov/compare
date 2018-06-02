# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0024_brand_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField()),
                ('seller', models.ForeignKey(to='diapers.Seller')),
            ],
        ),
    ]
