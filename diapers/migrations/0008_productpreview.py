# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0007_auto_20150824_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPreview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('url', models.TextField()),
                ('status', models.CharField(max_length=200)),
                ('brand', models.ForeignKey(to='diapers.Brand')),
                ('seller', models.ForeignKey(to='diapers.Seller')),
                ('series', models.ForeignKey(to='diapers.Series')),
            ],
        ),
    ]
