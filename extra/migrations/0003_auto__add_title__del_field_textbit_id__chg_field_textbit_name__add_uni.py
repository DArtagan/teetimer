# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Title'
        db.create_table('extra_title', (
            ('field', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('extra', ['Title'])

        # Deleting field 'TextBit.id'
        db.delete_column('extra_textbit', 'id')


        # Changing field 'TextBit.name'
        db.alter_column('extra_textbit', 'name', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True))
        # Adding unique constraint on 'TextBit', fields ['name']
        db.create_unique('extra_textbit', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'TextBit', fields ['name']
        db.delete_unique('extra_textbit', ['name'])

        # Deleting model 'Title'
        db.delete_table('extra_title')


        # User chose to not deal with backwards NULL issues for 'TextBit.id'
        raise RuntimeError("Cannot reverse this migration. 'TextBit.id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'TextBit.id'
        db.add_column('extra_textbit', 'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)


        # Changing field 'TextBit.name'
        db.alter_column('extra_textbit', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        'extra.textbit': {
            'Meta': {'object_name': 'TextBit'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        },
        'extra.title': {
            'Meta': {'object_name': 'Title'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['extra']