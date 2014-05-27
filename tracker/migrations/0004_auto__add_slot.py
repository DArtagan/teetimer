# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Slot'
        db.create_table('tracker_slot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('teetime', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.TeeTime'])),
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

        # Removing M2M table for field people on 'TeeTime'
        db.delete_table(db.shorten_name('tracker_teetime_people'))


    def backwards(self, orm):
        # Deleting model 'Slot'
        db.delete_table('tracker_slot')

        # Removing M2M table for field person on 'Slot'
        db.delete_table(db.shorten_name('tracker_slot_person'))

        # Adding M2M table for field people on 'TeeTime'
        m2m_table_name = db.shorten_name('tracker_teetime_people')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('teetime', models.ForeignKey(orm['tracker.teetime'], null=False)),
            ('user', models.ForeignKey(orm['accounts.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['teetime_id', 'user_id'])


    models = {
        'accounts.user': {
            'Meta': {'db_table': "'auth_user'", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tracker.slot': {
            'Meta': {'object_name': 'Slot'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.User']", 'null': 'True', 'blank': 'True', 'symmetrical': 'False'}),
            'teetime': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tracker.TeeTime']"})
        },
        'tracker.teetime': {
            'Meta': {'object_name': 'TeeTime'},
            'date_edited': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slots': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['tracker']