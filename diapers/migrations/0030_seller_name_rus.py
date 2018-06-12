# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0029_auto_20180612_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='name_rus',
            field=models.CharField(default='-1', max_length=200),
            preserve_default=False,
        ),
    ]
