# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('lid_number', models.CharField(max_length=64)),
                ('decade', models.IntegerField()),
                ('sex', models.CharField(max_length=1)),
                ('postcode_start', models.CharField(max_length=1)),
                ('subscription_year', models.IntegerField()),
                ('subscription_location', models.CharField(max_length=8)),
                ('category', models.CharField(max_length=8)),
            ],
            options={
                'db_table': 'borrowers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('borrowing_id', models.IntegerField()),
                ('from_date', models.CharField(max_length=10)),
                ('loan_period', models.IntegerField()),
                ('borrower', models.ForeignKey(to='apps4ghent.Borrower', db_column='borrower_id', related_name='borrowing_set')),
            ],
            options={
                'db_table': 'borrowings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('bbnr', models.IntegerField()),
                ('category_music', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=30)),
                ('title', models.TextField()),
                ('author_type', models.CharField(max_length=30)),
                ('isbn_wrong', models.CharField(max_length=50)),
                ('category_youth', models.CharField(max_length=50)),
                ('issn', models.CharField(max_length=30)),
                ('language', models.CharField(max_length=50)),
                ('ean', models.CharField(max_length=30)),
                ('age', models.CharField(max_length=30)),
                ('series_edition', models.CharField(max_length=255)),
                ('keywords_youth', models.CharField(max_length=128)),
                ('author_lastname', models.CharField(max_length=128)),
                ('publisher', models.CharField(max_length=255)),
                ('author_firstname', models.CharField(max_length=128)),
                ('keywords_libraries', models.CharField(max_length=128)),
                ('year_published', models.CharField(max_length=128)),
                ('keywords_local', models.CharField(max_length=128)),
                ('pages', models.CharField(max_length=255)),
                ('category_adults', models.CharField(max_length=64)),
                ('siso', models.CharField(max_length=64)),
                ('literarytype', models.CharField(max_length=64)),
                ('ean_wrong', models.CharField(max_length=64)),
                ('isbn', models.CharField(max_length=64)),
                ('issn_wrong', models.CharField(max_length=64)),
                ('siso_libraries', models.CharField(max_length=64)),
                ('avi', models.CharField(max_length=16)),
                ('openvlaccid', models.CharField(max_length=16)),
                ('keyword_adults', models.CharField(max_length=128)),
                ('zizo', models.CharField(max_length=16)),
                ('series_title', models.CharField(max_length=255)),
                ('keyword_youth', models.CharField(max_length=64)),
                ('na', models.TextField()),
            ],
            options={
                'db_table': 'items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemCopy',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('copy_id', models.CharField(max_length=32)),
                ('barcode', models.CharField(max_length=64)),
                ('nature', models.IntegerField()),
                ('copy_pk', models.CharField(max_length=128)),
                ('in_date', models.CharField(max_length=10)),
                ('item', models.ForeignKey(to='apps4ghent.Item', db_column='item_id', related_name='item_copy_set')),
            ],
            options={
                'db_table': 'items_copy',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('number', models.IntegerField()),
                ('cartodb_id', models.IntegerField()),
            ],
            options={
                'db_table': 'sectors',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='borrowing',
            name='item_copy',
            field=models.ForeignKey(to='apps4ghent.ItemCopy', db_column='item_copy_id', related_name='borrowing_set'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='borrower',
            name='sector',
            field=models.ForeignKey(to='apps4ghent.Sector', db_column='sector_id', related_name='borrower_set'),
            preserve_default=True,
        ),
    ]
