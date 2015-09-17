# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0008_productpreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreviewParseHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('preview', models.ForeignKey(to='diapers.ProductPreview')),
                ('product', models.ForeignKey(to='diapers.Product')),
            ],
        ),
    ]
