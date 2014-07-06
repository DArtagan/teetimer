# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Slot'
        db.delete_table('tracker_slot')

        # Removing M2M table for field person on 'Slot'
        db.delete_table(db.shorten_name('tracker_slot_person'))

        # Deleting field 'TeeTime.slots'
        db.delete_column('tracker_teetime', 'slots')

        # Adding M2M table for field person on 'TeeTime'
        m2m_table_name = db.shorten_name('tracker_teetime_person')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('teetime', models.ForeignKey(orm['tracker.teetime'], null=False)),
            ('user', models.ForeignKey(orm['accounts.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['teetime_id', 'user_id'])


    def backwards(self, orm):
        # Adding model 'Slot'
        db.create_table('tracker_slot', (
            ('teetime', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.TeeTime'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('tracker', ['Slot'])

        # Adding M2M table for field person on 'Slot'
        m2m_table_name = db.shorten_name('tracker_slot_person')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('slot', models.ForeignKey(orm['tracker.slot'], null=False)),
            ('user', models.ForeignKey(orm['accounts.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['slot_id', 'user_id'])


        # User chose to not deal with backwards NULL issues for 'TeeTime.slots'
        raise RuntimeError("Cannot reverse this migration. 'TeeTime.slots' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'TeeTime.slots'
        db.add_column('tracker_teetime', 'slots',
                      self.gf('django.db.models.fields.IntegerField')(),
                      keep_default=False)

        # Removing M2M table for field person on 'TeeTime'
        db.delete_table(db.shorten_name('tracker_teetime_person'))


    models = {
        'accounts.user': {
            'Meta': {'object_name': 'User', 'db_table': "'auth_user'"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tracker.teetime': {
            'Meta': {'object_name': 'TeeTime'},
            'date_edited': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'null': 'True', 'to': "orm['accounts.User']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['tracker']