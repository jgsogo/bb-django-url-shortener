# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Link'
        db.create_table(u'chimp_shortener_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_hash', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'chimp_shortener', ['Link'])


    def backwards(self, orm):
        # Deleting model 'Link'
        db.delete_table(u'chimp_shortener_link')


    models = {
        u'chimp_shortener.link': {
            'Meta': {'object_name': 'Link'},
            '_hash': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['chimp_shortener']